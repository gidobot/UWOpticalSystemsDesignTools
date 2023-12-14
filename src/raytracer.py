__author__ = 'Gideon Billings'

import numpy as np
import logging
from main import Model
from lights import LightSource
import math
import sys
from multiprocessing import Pool
import cv2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import argparse
import os

class Raytracer:
    def __init__(self, model):
        self.model = model

        # create initial planar depth map at 2 meters depth
        self.depth_map = np.ones((int(model.camera.sensor.resolution_y), int(model.camera.sensor.resolution_x))) * 1.16
        # create initial surface normal map with unit vector along negative z axis (towards camera)
        self.surface_normal_map = np.ones((int(model.camera.sensor.resolution_y), int(model.camera.sensor.resolution_x), 3)) * np.array([0.0, 0.0, -1.0])

    def compute_pixel_response_idx(self, i):
        px = i % int(self.model.camera.sensor.resolution_x)
        py = i // int(self.model.camera.sensor.resolution_x)
        logging.info("Computing pixel response for pixel {}/{}".format(i, int(self.model.camera.sensor.resolution_y)*int(self.model.camera.sensor.resolution_x)))
        signal, snr = self.compute_pixel_response(px, py)
        return signal

    def project_pixel_to_world(self, px, py):
        assert self.model.camera.initialized, "Camera must be initialized before projecting pixels to world coordinates."
        # compute projection of pixel into 3D world
        wz = self.depth_map[py, px] * 1000. # convert from m to mm
        pixel_size = self.model.camera.sensor.pixel_size * math.pow(10, -3) # convert from um to mm
        wx = (px - self.model.camera.sensor.resolution_x/2.0) * pixel_size * wz / self.model.camera.effective_focal_length
        wy = (py - self.model.camera.sensor.resolution_y/2.0) * pixel_size * wz / self.model.camera.effective_focal_length
        return np.array([wx/1000., wy/1000., wz/1000.])

    def compute_off_axis_angle(self, px, py):
        pw = self.project_pixel_to_world(px, py)
        pwd = pw/np.linalg.norm(pw)
        cos = np.dot(pwd, np.array([0.,0.,1.]))
        theta = np.arccos(cos)
        return theta

    def compute_off_axis_angle_map(self, projection_map, camera_distance_map):
        camera_distance_map = np.expand_dims(camera_distance_map, axis=-1)
        pwd = projection_map / np.tile(camera_distance_map, (1,1,3))
        cos = pwd[:,:,2]
        theta = np.arccos(cos)
        return theta

    def compute_off_axis_cos_angle_map(self, projection_map, camera_distance_map):
        camera_distance_map = np.expand_dims(camera_distance_map, axis=-1)
        pwd = projection_map / np.tile(camera_distance_map, (1,1,3))
        cos = pwd[:,:,2]
        return cos

    def compute_scene_light_map(self):
        assert self.model.camera.initialized and self.model.scene.water.initialized, "Camera and scene must be initialized."

        pixel_size = self.model.camera.sensor.pixel_size * math.pow(10, -3) # convert from um to mm

        z = self.depth_map * 1000. # convert from m to mm

        # create grid of pixel coordinates
        x, y = np.meshgrid(np.arange(self.model.camera.sensor.resolution_x), np.arange(self.model.camera.sensor.resolution_y))
        # compute projection of pixels into 3D world
        x = (x - self.model.camera.sensor.resolution_x/2.0) * pixel_size * z / self.model.camera.effective_focal_length
        y = (y - self.model.camera.sensor.resolution_y/2.0) * pixel_size * z / self.model.camera.effective_focal_length

        # stack the x, y, z coordinates to create a (height, width, 4) world homogeneous coordinate matrix
        projection_map = np.stack((x/1000.,y/1000.,z/1000.,np.ones(x.shape)), axis=-1)

        # compute light visibility maps
        total_radiance_spectrum_map = None
        for light in self.model.lights:
            assert light.initialized, "Light must be initialized."

            light_map, light_angle_map, light_distance_map = light.compute_visibility_map(projection_map)
            lights_wavelength, light_irradiance_spectrum_map = light.get_irradiance_spectrum_map(light_distance_map)
            water_attenuation_map = self.model.scene.water.get_attenuation_map(lights_wavelength, light_distance_map)
            surface_irradiance_map = light_irradiance_spectrum_map * water_attenuation_map

            # compute light radiance from surface
            # Lambertian Diffuse BRDF: http://www.joshbarczak.com/blog/?p=272
            # https://boksajak.github.io/files/CrashCourseBRDF.pdf
            cos_map = np.cos(light.compute_incident_angle_map(projection_map[:,:,:-1], self.surface_normal_map)) * light_map # mask spot coverage
            cos_map = np.expand_dims(cos_map, axis=-1)
            cos_map = np.tile(cos_map, (1,1,lights_wavelength.shape[0]))
            radiance_spectrum_map = surface_irradiance_map * cos_map * self.model.scene.get_reflectance() / np.pi
            if total_radiance_spectrum_map is None:
                total_radiance_spectrum_map = radiance_spectrum_map
            else:
                # currently assumes lights_wavelength is same for every light source
                total_radiance_spectrum_map = total_radiance_spectrum_map + radiance_spectrum_map

        # compute distance of each projected pixel world point to the camera
        camera_distance_map = np.linalg.norm(projection_map[:,:,:-1], axis=-1)
        # compute attenuation of light from scene to camera
        water_attenuation_map = self.model.scene.water.get_attenuation_map(lights_wavelength, camera_distance_map)
        # attenuated spectrum incident on camera
        cam_incident_radiance_map = total_radiance_spectrum_map * water_attenuation_map
        # fundamental radiometric relation
        # alpha_map = self.compute_off_axis_angle_map(projection_map[:,:,:-1], camera_distance_map)
        cos_alpha_map = self.compute_off_axis_cos_angle_map(projection_map[:,:,:-1], camera_distance_map)

        lens_transmittance = [self.model.camera.lens.get_transmittance(x) for x in lights_wavelength]
        sensor_irradiance_map = lens_transmittance * self.model.camera.lens.fundamental_radiometric_relation_map(cam_incident_radiance_map, self.model.aperture, cos_alpha_map)

        # TODO: Currently assumes all sensor parameters given relative to 16bit pixel response
        # digital_response_map = (self.model.camera.sensor.compute_digital_signal_broadband_map(self.model.exposure,
        digital_response_map, absorbed_photons_map = self.model.camera.sensor.compute_digital_signal_broadband_color_map(self.model.exposure,
                                                                            lights_wavelength,
                                                                            sensor_irradiance_map)

        snr_map, snr_ideal_map = self.model.camera.sensor.compute_signal_to_noise_ratio(absorbed_photons_map)

        return digital_response_map, snr_map, snr_ideal_map

    def compute_pixel_response(self, px, py):
        assert self.model.camera.initialized and self.model.scene.water.initialized, "Camera and scene must be initialized."

        pw = self.project_pixel_to_world(px, py)

        total_radiance_spectrum = None
        for light in self.model.lights:
            assert light.initialized, "Light must be initialized."

            if not light.check_visibility(pw):
                continue

            theta = light.compute_incident_angle(pw, self.surface_normal_map[py, px, :])
            if theta > np.pi/2:
                continue

            # compute total scene radiance at projected pixel location
            light_to_scene_distance = light.compute_distance(pw)
            # flood light spectrum and irradiance range to world point
            lights_wavelength, light_irradiance_spectrum = light.get_irradiance_spectrum(light_to_scene_distance)
            water_attenuation = [self.model.scene.water.get_attenuation(x, light_to_scene_distance) for x in lights_wavelength]
            # attenuated spectrum incident on world point
            surface_irradiance = light_irradiance_spectrum * water_attenuation

            # compute light radiance from surface
            # Lambertian Diffuse BRDF: http://www.joshbarczak.com/blog/?p=272
            # https://boksajak.github.io/files/CrashCourseBRDF.pdf
            radiance_spectrum = surface_irradiance * np.cos(theta) * self.model.scene.get_reflectance() / np.pi

            if total_radiance_spectrum is None:
                total_radiance_spectrum = radiance_spectrum
            else:
                # currently assumes lights_wavelength is same for every light source
                total_radiance_spectrum = total_radiance_spectrum + radiance_spectrum

        if total_radiance_spectrum is None:
            logging.debug("No light sources visible from pixel {},{}".format(px, py))
            return 0., 0.

        print("total_radiance_spectrum: {}".format(total_radiance_spectrum))

        cam_to_scene_distance = np.linalg.norm(pw)
        # compute attenuation of light from scene to camera
        water_attenuation = [self.model.scene.water.get_attenuation(x, cam_to_scene_distance) for x in lights_wavelength]
        # attenuated spectrum incident on camera
        cam_incident_radiance = total_radiance_spectrum * water_attenuation
        alpha = self.compute_off_axis_angle(px, py)
        lens_transmittance = [self.model.camera.lens.get_transmittance(x) for x in lights_wavelength]
        sensor_irradiance = lens_transmittance * self.model.camera.lens.fundamental_radiometric_relation(cam_incident_radiance, self.model.aperture, alpha)

        print("sensor_irradiance: {}".format(sensor_irradiance))

        # TODO: Currently assumes all sensor parameters given relative to 16bit pixel response
        digital_response, absorbed_photons = self.model.camera.sensor.compute_digital_signal_broadband(self.model.exposure,
                                                                            lights_wavelength,
                                                                            sensor_irradiance)
        print("digital_response: {}".format(digital_response))
        snr, snr_ideal = self.model.camera.sensor.compute_signal_to_noise_ratio(absorbed_photons)
        print("snr: {}, snr_ideal: {}".format(snr, snr_ideal))

        return digital_response, snr

def test(args):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info('Started')

    model = Model()

    model.camera.sensor.load('../cfg/sensors/imx264C.json')
    # focal length, transmittance
    model.camera.lens.init_generic_lens(8., 0.9)
    # model.camera.lens.init_generic_lens(6., 0.9)

    ## Kraken light
    # light = LightSource()
    # light.init_generic_led_light(4000., 94.)
    # light.set_offset([-0.5, 0, 0])
    # light.set_orientation(np.radians([0, 30, 0]))
    # model.add_light(light)

    ## Lab lights
    light = LightSource()
    # light.init_generic_led_light(5000., 94.)
    light.load('../cfg/lights/lab_light.json')
    light.set_offset([-0.5, 0, 0])
    light.set_orientation(np.radians([0, 30, 0]))
    model.add_light(light)

    light2 = LightSource()
    # light2.init_generic_led_light(5000., 94.)
    light2.load('../cfg/lights/lab_light.json')
    light2.set_offset([0.5, 0, 0])
    light2.set_orientation(np.radians([0, -30, 0]))
    model.add_light(light2)

    ## Lab lights in air
    # light = LightSource()
    # light.load('../cfg/lights/lab_light_air.json')
    # light.set_offset([0, 0, 0])
    # light.set_orientation(np.radians([0, 0, 0]))
    # model.add_light(light)

    # model.scene.water.load_jerlovI_profile()
    # model.scene.water.load_pure_profile()
    # model.scene.water.load_tank_profile()
    # logging.info("Loaded tank profile")

    model.scene.water.load_air_profile()
    logging.info("Loaded air profile")

    model.exposure = args.exposure / 1.0e6
    # model.exposure = 0.01
    model.scene.speed = 0.001 
    model.scene.altitude = 1.14 # tank
    # model.scene.altitude = 1.94 # air
    model.scene.bottom_type = 'Perfect' # manually tune albedo
    # model.aperture = 1.4
    # model.aperture = 2.0
    # model.aperture = 2.8
    model.aperture = 2.5
    # model.aperture = 4.0
    # model.aperture = 8.0
    # model.aperture = 11.0
    # model.aperture = 16.0

    model.update()

    raytracer = Raytracer(model)

    # r, snr = raytracer.compute_pixel_response(1000, 1000)
    # print("Pixel response: {}, SNR: {}".format(r, snr))

    digital_response_map, snr_map, snr_ideal_map = raytracer.compute_scene_light_map()

    # reflectance = np.array([0.3, 0.45, 0.6])
    # reflectance = np.array([0.35, 0.55, 0.75]) # tank bottom
    reflectance = np.array([0.73, 0.73, 0.8]) # white target

    digital_response_map = digital_response_map * reflectance
    snr_map = snr_map * np.sqrt(reflectance)
    snr_ideal_map = snr_ideal_map * np.sqrt(reflectance)

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(121)
    ax1.imshow(digital_response_map)
    ax1.axis('off')
    fig1.subplots_adjust(wspace=0, hspace=0)

    # idx = digital_response_map.shape[0] // 2
    idx = 670
    # idx = 775
    px_row = digital_response_map[idx]

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(121)
    ax2.plot(px_row)
    colors = ['r', 'g', 'b']
    for i,j in enumerate(ax2.lines):
        j.set_color(colors[i])
    ax2.set_xlabel('Pixel')
    # set y label to % exposed
    ax2.set_ylabel('Digital response (% exposed)')

    snr_row = snr_map[idx]
    snr_ideal_row = snr_ideal_map[idx]
    ax22 = fig2.add_subplot(122)
    ax22.plot(snr_row)
    ax22.plot(snr_ideal_row,'--')
    colors = ['r', 'g', 'b','r','g','b']
    for i,j in enumerate(ax22.lines):
        j.set_color(colors[i])
    ax22.set_xlabel('Pixel')
    # set y label to % exposed
    ax22.set_ylabel('SNR')

    if args.image is not None:
        # read in raw 16bit tif image as float. Reads in saved channel order -> RGB
        ground_truth_img = cv2.imread(args.image, cv2.IMREAD_UNCHANGED).astype(np.float32) / 65535.0
        ax12 = fig1.add_subplot(122)
        ax12.imshow(ground_truth_img)
        ax12.axis('off')

        px_row_gt = ground_truth_img[idx]
        ax2.plot(px_row_gt, '--')
        colors = ['r', 'g', 'b']
        for i,j in enumerate(ax2.lines[3:]):
            j.set_color(colors[i])

    if args.save_path is not None:
        if not os.path.exists(args.save_path):
            os.makedirs(args.save_path)
        fig1.savefig(os.path.join(args.save_path,str(args.exposure)+'_imgs.png'), bbox_inches='tight')
        fig2.savefig(os.path.join(args.save_path,str(args.exposure)+'_plot.png'), bbox_inches='tight')

    if not args.quiet:
        plt.show()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Test camera response raytracer')
    parser.add_argument('-i', '--image', type=str, help='Path to ground truth response image', required=False, default=None)
    parser.add_argument('-e', '--exposure', type=float, help='Exposure value in us', required=True)
    parser.add_argument('-s', '--save_path', type=str, help='Save path', required=False, default=None)
    parser.add_argument('-q', '--quiet', help='Do not show plots', action='store_true', required=False)
    return parser.parse_args()

if __name__=="__main__":
    args = parse_arguments()
    test(args)