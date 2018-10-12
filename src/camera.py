__author__ = 'eiscar'
import numpy as np
import json
import math
from scipy.integrate import simps
import matplotlib.pyplot as plt


import logging
logger = logging.getLogger(__name__)

class Sensor:
    def __init__(self):

        self.name = None

        self.resolution_x = 0
        self.resolution_y = 0

        self.pixel_size = 0  # in micro meters

        self.max_shutter_time = 0 # In micro seconds
        self.min_shutter_time = 0 # In micro seconds

        self.quantum_efficiency_wav = []
        self.quantum_efficiency = []  # List of tuples with wavelength,quantum_efficiency

        self.dark_noise = 0  # In Electrons

        self.initialized = False

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
                self.mode = sensor_data["mode"]
                self.resolution_y = float(sensor_data["resolution_y"])
                self.resolution_x = float(sensor_data["resolution_x"])
                self.pixel_size = float(sensor_data["pixel_size"])

                self.max_shutter_time = float(sensor_data["max_shutter_time"])
                self.min_shutter_time = float(sensor_data["min_shutter_time"])

                if self.mode == 'mono':
                    self.quantum_efficiency_wav = [float(x) for x in sensor_data["quantum_efficiency_wavelengths"]]
                    self.quantum_efficiency = [float(x) for x in sensor_data["quantum_efficiency"]]
                elif self.mode == 'color':
                    self.quantum_efficiency_wav = {}
                    self.quantum_efficiency = {}
                    self.quantum_efficiency_wav["red"] = [float(x) for x in sensor_data["quantum_efficiency_wavelengths"]["red"]]
                    self.quantum_efficiency_wav["green"] = [float(x) for x in sensor_data["quantum_efficiency_wavelengths"]["green"]]
                    self.quantum_efficiency_wav["blue"] = [float(x) for x in sensor_data["quantum_efficiency_wavelengths"]["blue"]]
                    self.quantum_efficiency["red"] = [float(x) for x in sensor_data["quantum_efficiency"]["red"]]
                    self.quantum_efficiency["green"] = [float(x) for x in sensor_data["quantum_efficiency"]["green"]]
                    self.quantum_efficiency["blue"] = [float(x) for x in sensor_data["quantum_efficiency"]["blue"]]
                    self.quantum_efficiency_wav["mono"], self.quantum_efficiency["mono"] = \
                        self.compute_combined_color_quantum_efficiency()
                    # fig1, ax1 = plt.subplots()
                    # ax1.plot(self.quantum_efficiency_wav["mono"], self.quantum_efficiency["mono"], '--x')
                    # plt.show()
                else:
                    return False

                self.dark_noise = float(sensor_data["dark_noise"])
                self.gain = float(sensor_data["gain"])
                print(self.gain)

            except KeyError as e:
                print("Error parsing json data for sensor. Key not found:",e)

        self.initialized = True
        return True

    def get_coc(self):
        """
        Compute the sensor sensor circle of confusion
        :return: Sensor diagonal in mm
        """
        sensor_diagonal = math.sqrt(self.get_sensor_size('x')**2 + self.get_sensor_size('y')**2)
        sensor_diagonal /= 1000  # Convert to mm

        coc = sensor_diagonal / 1500
        return coc

    def get_quantum_efficiency(self, wave_length):
        """
        Interpolate Quantum efficiency value for a given wavelength
        :param wave_length: Input wavelength
        :return:
        """
        if self.mode == 'mono':
            return np.interp(wave_length, self.quantum_efficiency_wav, self.quantum_efficiency)
        elif self.mode == 'color':
            return np.interp(wave_length, self.quantum_efficiency_wav["mono"], self.quantum_efficiency["mono"])

    def compute_combined_color_quantum_efficiency(self):
        """
        Calculate mono quantum efficiency response for color camera from individual
        color channel quantum efficiency curves.
        param red_wav: Red channel wavelengths
        param green_wav: Green channel wavelengths
        param blue_wav: Blue channel wavelengths
        param red_eff: Red channel quantum efficiency
        param green_eff: Green channel quantum efficiency
        param blue_eff: Blue channel quantum efficiency
        return: Wavelengths for combined mono response,
                Combined quantum efficiency for mono response
        """
        mono_wav = np.array(self.quantum_efficiency_wav["green"], dtype=float)
        red = np.array([np.interp(x, self.quantum_efficiency_wav["red"], self.quantum_efficiency["red"]) for x in mono_wav], dtype=float)
        green = np.array(self.quantum_efficiency["green"], dtype=float)
        blue = np.array([np.interp(x, self.quantum_efficiency_wav["blue"], self.quantum_efficiency["blue"]) for x in mono_wav], dtype=float)
        mono_eff = (2*green + red + blue)/4
        return mono_wav, mono_eff

    def compute_incident_photons(self, wavelength, exposure_time, irradiance):
        """
        Compute the amount of incident photons for narrowband light
        :param wavelength: wavelength of incident light in [nm]
        :param exposure_time: image shutter time in [s]
        :param irradiance:  Incident Radiance E on sensor surface in [W/m^2*nm]
        :return: Number of incident photons
        """
        exposure_time = exposure_time*math.pow(10,3)
        irradiance = irradiance * wavelength * math.pow(10,2) # from [W/m^2*nm] to [uW/cm^2]
        wavelength = wavelength*math.pow(10,-3) # from nm to um
        pixel_area = self.get_pixel_area('um')
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

    def compute_absorbed_photons_broadband(self, wavelengths, incident_spectrum, exposure_time):
        """
        Compute the number of incident photons for broadband light defined as a spectrum
        :param wavelengths: Array of wavelengths in nm
        :param incident_spectrum: Array with incident light spectrum defined in W/(m2nm)
        :param exposure_time: Exposure time of image in seconds
        :return:
        """
        h = 6.62607004 * math.pow(10, -34)  # Plancks constant (m2kg)/s
        c = 299792458  # speed of light in m/s

        # Weight the spectrum with the quantum efficiency curve
        quantum_eff_spectrum = [self.get_quantum_efficiency(x) for x in wavelengths]    # Units: Dimensionless
        absorbed_spectrum = np.multiply(quantum_eff_spectrum, incident_spectrum)        # Units: W/(m2nm)

        # Weight the spectrum with the wavelength
        lambda_spectrum = np.multiply(wavelengths, absorbed_spectrum)  # W/m2

        integral = simps(lambda_spectrum, np.array(wavelengths)*math.pow(10, -9))  # W/m
        photon_density = integral / (h*c)  # Photons/m2s
        photons = photon_density * self.get_pixel_area('m') * exposure_time
        # print(self.get_pixel_area('m'))
        return photons

    def compute_digital_signal_broadband(self, exposure_time, wavelengths, incident_spectrum):
        """
        Compute the output digital signal
        :param gain: Gain of sensor
        :param exposure_time: Exposure time of image in s
        :param wavelengths: Array of wavelengths in nm
        :param incident_spectrum: Spectrum of incident light in W/(nmm2)
        :return:
        """
        photons = self.compute_absorbed_photons_broadband(wavelengths, incident_spectrum, exposure_time)
        signal = self.gain * (self.dark_noise+photons)
        return signal

    def compute_digital_signal(self, exposure_time, wavelength, irradiance):
        """
        Compute the digital signal value
        :param Gain: Overall system gain in DN/e- (digits per electron)
        :param wavelength:  wavelength of incident light in [um]
        :param exposure_time: image shutter time in [ms]
        :param irradiance: Incident Radiance E on sensor surface in [uW/cm^2]
        :return: Mean digital signal
        """
        signal = self.gain*(self.dark_noise+self.compute_absorbed_photons(wavelength, exposure_time, irradiance))
        return signal

    def get_sensor_size(self, axis):
        """
        Compute the sensor size in micrometers
        :param axis: Sensor axis
        :return: Size along the specified axis im um
        """
        return self.get_resolution(axis) * self.pixel_size

    def get_pixel_area(self, units='mm'):
        """ Compute the area of a pixel in um2
        :param: Units: Either 'm', 'mm', 'um'
        :return: Pixel area in um2
        """
        if units == 'm':
            return (self.pixel_size*math.pow(10, -6))**2
        if units == 'mm':
            return (self.pixel_size*math.pow(10, -3))**2
        if units == 'um':
            return (self.pixel_size)**2

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
        self.focal_length = 0  # In [mm]
        self.transmittance_wav = []
        self.transmittance = []  # Tuples of wavelength and transmittance (nm, %1)

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

                self.transmittance = [float(x) for x in lens_data["transmittance"]]
                self.transmittance_wav = [float(x) for x in lens_data["transmittance_wavelength"]]

            except KeyError as e:
                logger.error("Error parsing json data for lens. Key not found:", e)

        self.initialized = True
        return True

    def get_transmittance(self, wave_length):
        """
        Interpolate transmittance value
        :param wave_length:
        :return: Transmittance at given wavelength as a fraction
        """
        return np.interp(wave_length, self.transmittance_wav, self.transmittance)

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
        self.transmittance_wav = range(400, 1001, 50)
        self.transmittance = [t] * 13
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

        self.housing = 'flat'

    @property
    def effective_focal_length(self):
        """
        Effect of underwater housings on focal length, from Lavest et al "Underwater Camera Calibration"
        :return:
        """
        if self.housing == 'flat':
            return self.lens.focal_length*1.33
        elif self.housing == 'domed':
            return self.lens.focal_length

    def set_housing(self, housing_type):
        """
        Set the type of housing the camera is located in. Flat viewports affect the focal length
        :param housing_type: Either 'flat' or 'domed'
        :return: None
        """
        if housing_type == 'flat':
            self.housing = housing_type
        elif housing_type == 'domed':
            self.housing = housing_type
        else:
            logger.error("Undefined housing type")

    def initialized(self):
        """
        Test if both sensor and lens have been initialized
        :return: True or False
        """

        return self.sensor.initialized and self.lens.initialized

    def get_angular_fov(self, axis):
        """
        Get the angular field of view in radians on the specified axis
        :param axis: Either x or y
        :return: FOV in radians
        """
        fov = 2 * np.arctan2(self.sensor.get_sensor_size(axis)/1000, 2*self.effective_focal_length)
        logger.debug("Angular FOV: %f", fov)
        return fov

    def get_fov(self, axis, working_distance):
        """
        Get the size of the area covered by the image
        :param axis: x or y
        :param working_distance: Distance between the camera and the subject
        :return: size of the area covered by the image along the given axis in the same units as working distance
        """
        if self.initialized():
            fov = 2 * working_distance * np.tan(self.get_angular_fov(axis)/2)
            return fov
        else:
            logger.error("Tried to cpmpute camera FOV without initializing sensor or lens")
            return -1

    def max_blur_shutter_time(self, axis, working_distance, camera_speed, blur):
        """
        Compute the maximum exposure time to ensure motion smaller than the specified value
        :param axis: Axis (x or y) along which the camera is moving
        :param working_distance: Distance between the camera and the subject, in m
        :param camera_speed: Speed of the camera movement along the specified axis in m/s
        :param blur: Maximum allowable motion blur in pixels
        :return:
        """
        if camera_speed <= 0:
            logger.error("Vehicle speed has to be positive for exposure calculation")
            return 0
        pixel_res = self.sensor.get_resolution(axis)/self.get_fov(axis, working_distance)
        pixel_speed = camera_speed * pixel_res
        max_shutter_time = blur/pixel_speed
        return max_shutter_time

    def compute_depth_of_field(self, lens_aperture, focus_distance):
        f = self.effective_focal_length
        c = self.sensor.get_circle_of_confusion()
        dof = (2*lens_aperture*c*f**2*focus_distance**2) / (f**4-lens_aperture**2*c**2*focus_distance**2)
        return dof

    def compute_aperture(self, dof, working_distance):
        """
        Equation from https://en.wikipedia.org/wiki/Depth_of_field
        :param coc: Circle of confusion: specs the allowable blur, in mm
        :param dof: desired depth of field, in m
        :param working_distance: Distance at which the camera is focused
        :return:
        """
        logger.debug("Computing aperture")
        coc = self.sensor.get_coc()
        df = (working_distance + dof/2) * 1000  # Convert to mm
        dn = (working_distance - dof/2) * 1000  # Convert to mm
        f = self.effective_focal_length

        N = (f**2/coc)*((df-dn)/(df*(dn-f) + dn*(df-f)))
        return N

    def compute_framerate(self, axis, working_distance, speed, overlap):
        """
        Compute the required framerate for a camera
        :param axis: Axis (x or y) along which the camera is moving
        :param working_distance: Distance between the camera and the subject, in m
        :param speed:  Speed of the camera movement along the specified axis in m/s
        :param overlap: Amount of overlap desired as a fraction (0-1)
        :return: Required framerate in Hz
        """
        if overlap > 1 or overlap < 0:
            logger.error("Overlap out of bounds for framerate calculation")
            return 0
        if working_distance < 0:
            logger.error("Working distance out of bounds for framerate calculation")
        f = speed / (self.get_fov(axis, working_distance)*(1-overlap))
        return f





class OperationalParameters:
    def __init__(self):
        self.altitude = None
        self.overlap = None
        self.speed = None
        self.motion_blur = None
        self.depthoffield = None
        self.bottom_type = None

        self.axis = 'x'

    def initialize(self, alt, ovr, spe, mot, dep, bot):
        self.altitude = alt
        self.overlap = ovr
        self.speed = spe
        self.motion_blur = mot
        self.depthoffield = dep
        self.bottom_type = bot


class Reflectance:
    def __init__(self):
        self.wavelengths = []
        self.reflectance = []

    def load(self):
        pass

