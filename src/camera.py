__author__ = 'eiscar'
import numpy as np
import scipy
import json

import logging
logger = logging.getLogger(__name__)

class Sensor:
    def __init__(self):

        self.name = None

        self.resolution_x = None
        self.resolution_y = None

        self.pixel_size = None  # in micro meters

        self.max_shutter_time = None
        self.min_shutter_time = None

        self.quantum_efficiency = [(), ()]  # List of tuples with wavelength,quantum_efficiency

        self.dark_noise = None  # In Electrons

    def load(self, file_path):
        """
        Load json with Sensor parameters
        :param filepath: Path to the JSON file
        :return: true if loaded correctly, false otherwise
        """
        with open(file_path) as f:
            sensor_data = json.load(f)
            try:
                if not sensor_data["type"] == "sensor":
                    return False
                self.name = sensor_data["name"]
                self.resolution_y = float(sensor_data["resolution_y"])
                self.resolution_x = float(sensor_data["resolution_x"])
                self.pixel_size = float(sensor_data["pixel_size"])

                self.max_shutter_time = float(sensor_data["max_shutter_time"])
                self.min_shutter_time = float(sensor_data["min_shutter_time"])

                self.quantum_efficiency = zip(sensor_data["quantum_efficiency_wavelengths"],
                                              sensor_data["quantum_efficiency"])

                self.dark_noise = float(sensor_data["dark_noise"])

            except KeyError as e:
                print("Error parsing json data for sensor. Key not found:",e)
        return True

    def get_quantum_efficiency(self, wave_length):
        """
        Interpolate Quantum efficiency value for a
        :param wave_length:
        :return:
        """
        wave_lengths = map(lambda x: x[0], self.quantum_efficiency)
        quantum_efficiencies = map(lambda x: x[1], self.quantum_efficiency)
        return np.interp(wave_length, wave_lengths, quantum_efficiencies)

    def compute_incident_photons(self, wavelength, exposure_time, irradiance):
        """
        Compute the amount of incident photons
        :param wavelength: wavelength of incident light in [um]
        :param exposure_time: image shutter time in [ms]
        :param irradiance:  Incident Radiance E on sensor surface in [uW/cm^2]
        :return: Number of incident photons
        """
        pixel_area = self.pixel_size**2
        incident_photons = 50.34 * pixel_area * exposure_time * wavelength * irradiance
        return incident_photons

    def compute_absorbed_photons(self, wavelength, exposure_time, irradiance):
        """
        Compute the number of absorbed photons
        :param wavelength:  wavelength of incident light in [um]
        :param exposure_time: image shutter time in [ms]
        :param irradiance: Incident Radiance E on sensor surface in [uW/cm^2]
        :return: Number of absorbed photons
        """
        quantum_efficiency = self.get_quantum_efficiency(wavelength)
        absorbed_photons = quantum_efficiency * self.compute_incident_photons(wavelength, exposure_time, irradiance)
        return absorbed_photons

    def compute_digital_signal(self, Gain, wavelength, exposure_time, irradiance):
        """
        Compute the digital signal value
        :param Gain: Overall system gain in DN/e- (digits per electron)
        :param wavelength:  wavelength of incident light in [um]
        :param exposure_time: image shutter time in [ms]
        :param irradiance: Incident Radiance E on sensor surface in [uW/cm^2]
        :return: Mean digital signal
        """
        signal = Gain*(self.dark_noise+self.compute_absorbed_photons(wavelength, exposure_time, irradiance))
        return signal

    def get_sensor_size(self, axis):
        """
        Compute the sensor size in micrometers
        :param axis: Sensor axis
        :return: Size along the specified axis im um
        """
        return self.get_resolution(axis) * self.pixel_size

    def get_resolution(self, axis):
        """
        Get the resolution along the specified axis
        :param axis: x or y
        :return: resolution in pixels along the axis
        """
        if axis == "x":
            return self.resolution_x
        elif axis == "y":
            return self.resolution_y
        else:
            raise ValueError("Axis has to be either x or y")

    def get_circle_of_confusion(self):
        """
        Compute the acceptable size for the circle of confusion based on sensor size. Approximation
        :return: Circle of confusion size in mm
        """
        sensor_diag = np.sqrt( self.get_sensor_size('x')**2 + self.get_sensor_size('y')**2) / 1000
        coc = sensor_diag / 1500
        return coc


class Lens:
    def __init__(self):
        self.name = None
        self.focal_length = None  # In [mm]
        self.transmittance = [(), ()] # Tuples of wavelength and transmittance (nm, %1)

        self.initialized = False

    def load(self, file_path):
        """
        Load json with lens parameters
        :param filepath: Path to the JSON file
        :return: true if loaded correctly, false otherwise
        """
        logger.debug('Loading file for lens class: %s', file_path)
        with open(file_path) as f:
            lens_data = json.load(f)
            try:
                if not lens_data["type"] == "lens":
                    logger.error("Incorrect data file passed to lens loader")
                    return False
                self.name = lens_data["name"]
                self.focal_length = float(lens_data["focal_length"])
                self.transmittance = zip(lens_data["transmittance_wavelength"],
                                         lens_data["transmittance"])

            except KeyError as e:
                logger.error("Error parsing json data for lens. Key not found:", e)

        self.initialized = True
        return True

    def fundamental_radiometric_relation(self, L, N, alfa):
        """
        Fundamental Radiometric relation between scene radiance L and the light Irradiance E reaching the pixel sensor
        :param L: Scene Radiance
        :param N: Lens Aperture
        :param alfa: Off-Axis Angle
        :return: Irradiance reaching the pixel sensor
        """
        E = L*(np.pi/4)*((1/N)**2)*np.cos(alfa)**4
        return E

    def get_aperture_diameter(self, N):
        """
        Compute the lens aperture diameter
        :param N: Lens aperture number
        :return: Diameter of lens aperture in mm
        """
        d = self.focal_length/N
        return d

    def init_generic_lens(self, f, t):
        """
        Initialize a generic lens based on the given focal length and constant transmittance value
        :param f: Focal length in mm
        :param t: Transmittance as a fraction
        :return: True if successful, False otherwise
        """
        self.focal_length = f
        if t > 1:
            logger.error("Transmittance value of %f bigger then 1", t)
            return False
        self.transmittance = zip(list(range(400, 1001, 50)), [t] * 13)
        self.initialized = True
        return True

    def reset(self):
        """
        Reset the class to original state
        :return: None
        """
        self.__init__()


class Camera:
    def __init__(self):
        self.sensor = Sensor()
        self.lens = Lens()

    def get_angular_fov(self, axis):
        """
        Get the angular field of view in radians on the specified axis
        :param axis: Either x or y
        :return: FOV in radians
        """
        fov = np.arctan2(self.sensor.get_sensor_size(axis)/1000, 2*self.lens.focal_length)
        return fov

    def get_fov(self, axis, working_distance):
        """
        Get the size of the area covered by the image
        :param axis: x or y
        :param working_distance: Distance between the camera and the subject, in mm
        :return: size of the area covered by the image along the given axis
        """
        horizontal_fov = 2 * working_distance * np.tan(self.get_angular_fov(axis)/2)
        return horizontal_fov

    def max_blur_shutter_time(self,axis, working_distance, camera_speed, blur):
        """
        Compute the maximum exposure time to ensure motion smaller than the specified value
        :param axis: Axis (x or y) along which the camera is moving
        :param working_distance: Distance between the camera and the subject, in mm
        :param camera_speed: Speed of the camera movement along the specified axis in mm/s
        :param blur: Maximum allowable motion blur in pixels
        :return:
        """
        pixel_res = self.sensor.get_resolution(axis)/self.get_horizontal_fov(axis, working_distance)
        pixel_speed = camera_speed * pixel_res
        max_shutter_time = blur/pixel_speed
        return max_shutter_time

    def compute_depth_of_field(self, lens_aperture, focus_distance):
        f = self.lens.focal_length
        c = self.sensor.get_circle_of_confusion()
        dof = (2*lens_aperture*c*f**2*focus_distance**2) / (f**4-lens_aperture**2*c**2*focus_distance**2)
        return dof


class LightSource:
    def __init__(self):
        self.name = None
        self.luminousflux = None
        self.beam_angle = None
        self.spectral_dist = [(), ()]  # Spectral distribution of the light source as list of tuples
        self.initialized = False

    def compute_peak_wavelength(self, T):
        """
        Compute the peak wavelength for a given light temperature in degrees Kelvin using Wiens displacement law
        :param T: Light temperature in K
        :return:  Wavelength in nm
        """
        b = 2.8977729*pow(10, -3)
        wav_length = (b/T) * pow(10, 9)
        return wav_length

    def get_photopic_eff(self):
        """
        Return a list of tuples containing the photopic efficiency curve.
        Data obtained from http://www.cvrl.org/lumindex.htm (CIE Photopic V(λ) modified by Judd (1951))
        :return: List of tuples. First element in tuple wavelength in nm, second element photopic efficiency
        """
        photopic_eff = [(370,    0.0001), (380,    0.0004), (390,    0.0015), (400,    0.0045), (410,    0.0093),
                        (420,    0.0175), (430,    0.0273), (440,    0.0379), (450,    0.0468), (460,    0.0600),
                        (470,    0.0910), (480,    0.1390), (490,    0.2080), (500,    0.3230), (510,    0.5030),
                        (520,    0.7100), (530,    0.8620), (540,    0.9540), (550,    0.9950), (560,    0.9950),
                        (570,    0.9520), (580,    0.8700), (590,    0.7570), (600,    0.6310), (610,    0.5030),
                        (620,    0.3810), (630,    0.2650), (640,    0.1750), (650,    0.1070), (660,    0.0610),
                        (670,    0.0320), (680,    0.0170), (690,    0.0082), (700,    0.0041), (710,    0.0021),
                        (720,    0.0011), (730,    0.0005), (740,    0.0002), (750,    0.0001), (760,    0.0001),
                        (770,    0.0000)]
        return photopic_eff

    def load(self, file_path):
        """
        Load json with Sensor parameters
        :param filepath: Path to the JSON file
        :return: true if loaded correctly, false otherwise
        """
        with open(file_path) as f:
            light_data = json.load(f)
            try:
                if not light_data[type] == "Light":
                    return False

                self.name = light_data["name"]

                self.beam_angle = light_data["beam_angle"]
                self.luminous_flux = light_data["luminous_flux"]
                self.spectral_dist = zip(light_data["wavelengths"],
                                         light_data["spectral_distribution"])

            except KeyError as e:
                print("Error parsing json data for sensor. Key not found:",e)

    def init_generic_led_light(self, luminous_flux, beam_angle):
        self.name = "Generic LED"

        # Led parameters (mean_1, mean_2, std_1, std_2, scale_1, scale_2)
        params = [450.70, 565.43, 11.67,  64.63,  24.49, 119.86]
        m1, m2, s1, s2, k1, k2 = params
        wavelength = np.linspace(400, 801, 600)
        sp_eff = k1*scipy.stats.norm.pdf(wavelength, loc=m1, scale=s1) + \
                 k2*scipy.stats.norm.pdf(wavelength, loc=m2, scale=s2)
        self.spectral_dist = zip(wavelength, sp_eff)

        try:
            self.luminousflux = int(luminous_flux)
            self.beam_angle = int(beam_angle)
        except ValueError:
            logger.error("Passed wrong type variable to generic led initialization")

        self.initialized = True

class WaterPropagation:
    def __init__(self):
        pass

class OperationalParameters:
    def __init__(self):
        self.altitude = None
        self.overlap = None
        self.speed = None
        self.motion_blur = None
        self.depthoffield = None
        self.bottom_type = None

    def initialize(self, alt, ovr, spe, mot, dep, bot):
        self.altitude = alt
        self.overlap = ovr
        self.speed = spe
        self.motion_blur = mot
        self.depthoffield = dep
        self.bottom_type = bot

if __name__ == "__main__":
    light = LightSource()
    print(light.compute_peak_wavelength(5778.0))
    image_sensor = Sensor()
    image_sensor.load("/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/cfg/database.json")
    print(list(image_sensor.quantum_efficiency))
