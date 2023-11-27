__author__ = 'Gideon Billings'

import numpy as np
import logging
from main import Model
from lights import LightSource
import math
import sys
from multiprocessing import Pool
import cv2

class Raytracer:
    def __init__(self, model):
        self.model = model

        # create initial planar depth map at 2 meters depth
        self.depth_map = np.ones((int(model.camera.sensor.resolution_y), int(model.camera.sensor.resolution_x))) * 2.0
        # create initial surface normal map with unit vector along negative z axis (towards camera)
        self.surface_normal_map = np.ones((int(model.camera.sensor.resolution_y), int(model.camera.sensor.resolution_x), 3)) * np.array([0.0, 0.0, -1.0])

    def render(self):
        assert self.model.camera.initialized and self.model.scene.water.initialized, "Camera and scene must be initialized."
        # initialize rendered image
        rendered_image = np.zeros((int(self.model.camera.sensor.resolution_y), int(self.model.camera.sensor.resolution_x)))
        snr_map        = np.zeros((int(self.model.camera.sensor.resolution_y), int(self.model.camera.sensor.resolution_x)))
        # iterate over all pixels in image
        num_pixels = int(self.model.camera.sensor.resolution_y) * int(self.model.camera.sensor.resolution_x)

        pool = Pool(processes=20)
        results = pool.map(self.compute_pixel_response_idx, range(num_pixels))
        
        pool.close()
        pool.join()

        print(results)
        # for py in range(int(self.model.camera.sensor.resolution_y)):
            # for px in range(int(self.model.camera.sensor.resolution_x)):
                # logging.info("Computing pixel response for pixel {}/{}".format(py*int(self.model.camera.sensor.resolution_x) + px, num_pixels))
                # compute pixel response
                # rendered_image[py, px], snr_map[py, px] = self.compute_pixel_response(px, py)
        return rendered_image, snr_map

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
            # cos_map = np.cos(light_angle_map) * light_map # mask spot coverage
            cos_map = np.cos(light.compute_incident_angle_map(projection_map[:,:,:-1], self.surface_normal_map)) * light_map # mask spot coverage
            cos_map = np.expand_dims(cos_map, axis=-1)
            cos_map = np.tile(cos_map, (1,1,lights_wavelength.shape[0]))
            radiance_spectrum_map = surface_irradiance_map * cos_map * self.model.scene.get_reflectance() / np.pi
            if total_radiance_spectrum_map is None:
                total_radiance_spectrum_map = radiance_spectrum_map
            else:
                # currently assumes lights_wavelength is same for every light source
                total_radiance_spectrum_map = total_radiance_spectrum_map + radiance_spectrum_map

            # plot light map image to window that fits screen
            # cv2.namedWindow("Light Map", cv2.WINDOW_NORMAL)
            # cv2.imshow("Light Map", light_map.astype(np.uint8) * 255)
            # # cv2.imshow("Light Map", np.ones(light_angle_map.shape) - light_angle_map / np.max(light_angle_map))
            # cv2.resizeWindow("Light Map", 800, 800)

        # compute distance of each projected pixel world point to the camera
        camera_distance_map = np.linalg.norm(projection_map[:,:,:-1], axis=-1)
        # compute attenuation of light from scene to camera
        water_attenuation_map = self.model.scene.water.get_attenuation_map(lights_wavelength, camera_distance_map)
        # attenuated spectrum incident on camera
        cam_incident_radiance_map = total_radiance_spectrum_map * water_attenuation_map
        # fundamental radiometric relation
        alpha_map = self.compute_off_axis_angle_map(projection_map[:,:,:-1], camera_distance_map)
        lens_transmittance = [self.model.camera.lens.get_transmittance(x) for x in lights_wavelength]
        sensor_irradiance_map = lens_transmittance * self.model.camera.lens.fundamental_radiometric_relation_map(cam_incident_radiance_map, self.model.aperture, alpha_map)

        # TODO: Currently assumes all sensor parameters given relative to 12bit pixel response
        digital_response_map, absorbed_photons_map = self.model.camera.sensor.compute_digital_signal_broadband_map(self.model.exposure,
                                                                            lights_wavelength,
                                                                            sensor_irradiance_map)
        snr, snr_ideal = self.model.camera.sensor.compute_signal_to_noise_ratio(absorbed_photons_map)

        cv2.namedWindow("Digital Response", cv2.WINDOW_NORMAL)
        cv2.imshow("Digital Response", digital_response_map)
        # cv2.imshow("Digital Response", np.ones(digital_response_map.shape) - digital_response_map / np.max(digital_response_map))
        cv2.resizeWindow("Digital Response", 800, 800)
        cv2.waitKey(0)

        return digital_response_map

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

        # TODO: Currently assumes all sensor parameters given relative to 12bit pixel response
        digital_response, absorbed_photons = self.model.camera.sensor.compute_digital_signal_broadband(self.model.exposure,
                                                                            lights_wavelength,
                                                                            sensor_irradiance)
        print("digital_response: {}".format(digital_response))
        snr, snr_ideal = self.model.camera.sensor.compute_signal_to_noise_ratio(absorbed_photons)
        print("snr: {}, snr_ideal: {}".format(snr, snr_ideal))

        return digital_response, snr

def test():
    # logging.basicConfig(filename='/home/eiscar/myapp.log', level=logging.DEBUG, filemode='w')
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info('Started')

    model = Model()

    model.camera.sensor.load('../cfg/sensors/imx250C.json')
    # focal length, transmittance
    model.camera.lens.init_generic_lens(6., 0.9)

    # lumens, beam angle
    light = LightSource()
    light.init_generic_led_light(6000., 80.)
    light.set_offset([-1.2, 0, 0])
    light.set_orientation(np.radians([0, 30, 0]))
    model.add_light(light)

    light2 = LightSource()
    light2.init_generic_led_light(6000., 80.)
    light2.set_offset([1.2, 0, 0])
    light2.set_orientation(np.radians([0, -20, 0]))
    model.add_light(light2)

    model.scene.water.load_jerlov1C_profile()
    logging.info("Loaded Jerlov1C profile")

    model.exposure = 0.003
    model.scene.speed = 0.5

    model.update()

    raytracer = Raytracer(model)

    # r, snr = raytracer.compute_pixel_response(1000, 1000)
    # print("Pixel response: {}, SNR: {}".format(r, snr))

    # image, snr_map = raytracer.render()
    raytracer.compute_scene_light_map()

if __name__=="__main__":
    test()