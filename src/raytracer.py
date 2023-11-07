__author__ = 'gbillings'

import numpy as np
import logging
from main import Model
from lights import LightSource
import math
import sys
from multiprocessing import Pool

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

    def compute_pixel_response(self, px, py):
        assert self.model.camera.initialized and self.model.scene.water.initialized, "Camera and scene must be initialized."

        pw = self.project_pixel_to_world(px, py)

        total_radiance_spectrum = None
        for light in self.model.lights:
            assert light.initialized, "Light must be initialized."

            if not light.check_visibility(pw):
                continue

            theta = light.compute_incident_angle(pw, self.surface_normal_map[py, px])
            if theta > np.pi/2:
                continue

            # compute total scene radiance at projected pixel location
            light_to_scene_distance = light.compute_distance(pw)
            # flood light spectrum and irradiance range to world point
            lights_wavelength, light_irradiance_spectrum = light.get_irradiance_spectrum(light_to_scene_distance)
            water_attenuation = [self.model.scene.water.get_attenuation(x, light_to_scene_distance) for x in lights_wavelength]
            # attenuated spectrum incident on world point
            surface_irradiance = light_irradiance_spectrum * np.power(water_attenuation, 2)

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

        cam_to_scene_distance = np.linalg.norm(pw)
        # compute attenuation of light from scene to camera
        water_attenuation = [self.model.scene.water.get_attenuation(x, cam_to_scene_distance) for x in lights_wavelength]
        # attenuated spectrum incident on camera
        cam_incident_radiance = total_radiance_spectrum * np.power(water_attenuation, 2)
        alpha = self.compute_off_axis_angle(px, py)
        lens_transmittance = [self.model.camera.lens.get_transmittance(x) for x in lights_wavelength]
        sensor_irradiance = lens_transmittance * self.model.camera.lens.fundamental_radiometric_relation(cam_incident_radiance, self.model.aperture, alpha)

        # TODO: Currently assumes all sensor parameters given relative to 16bit pixel response
        digital_response = (self.model.camera.sensor.compute_digital_signal_broadband(self.model.exposure,
                                                                            lights_wavelength,
                                                                            sensor_irradiance)/2**16)*100
        snr = self.model.camera.sensor.compute_signal_to_noise_ratio(self.model.exposure, lights_wavelength, sensor_irradiance)

        return digital_response, snr

def test():
    # logging.basicConfig(filename='/home/eiscar/myapp.log', level=logging.DEBUG, filemode='w')
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info('Started')

    model = Model()

    model.camera.sensor.load('../cfg/sensors/imx250C.json')
    # focal length, transmittance
    model.camera.lens.init_generic_lens(8., 0.9)

    # lumens, beam angle
    light = LightSource()
    light.init_generic_led_light(20000., 60.)
    model.add_light(light)

    model.scene.water.load_jerlov1C_profile()
    logging.info("Loaded Jerlov1C profile")

    model.exposure = 0.01

    model.update()

    raytracer = Raytracer(model)

    image, snr_map = raytracer.render()

if __name__=="__main__":
    test()