__author__ = 'Gideon Billings'
import numpy as np
import json
import math
from scipy.integrate import simps, romb
import matplotlib
import matplotlib.pyplot as plt

import logging
logger = logging.getLogger(__name__)

class Sensor:
    def __init__(self):

        self.name = None

        self.resolution_x = 1000.
        self.resolution_y = 1000.

        self.pixel_size = 3.45  # in micro meters

        self.max_shutter_time = 2000000. # In micro seconds
        self.min_shutter_time = 20. # In micro seconds

        self.quantum_efficiency_wav = []
        self.quantum_efficiency_color = {}
        self.quantum_efficiency_wav_color = {}
        self.quantum_efficiency = []  # List of tuples with wavelength,quantum_efficiency

        self.dark_noise = 0.  # In Electrons
        self.dark_current = 0.  # In Electrons
        self.gain = 0.
        self.initialized = False
        self.user_gain = 1.

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
                    self.quantum_efficiency_wav_color = {}
                    self.quantum_efficiency_color = {}
                    self.quantum_efficiency_wav_color["red"] = [float(x) for x in sensor_data["quantum_efficiency_wavelengths"]["red"]]
                    self.quantum_efficiency_wav_color["green"] = [float(x) for x in sensor_data["quantum_efficiency_wavelengths"]["green"]]
                    self.quantum_efficiency_wav_color["blue"] = [float(x) for x in sensor_data["quantum_efficiency_wavelengths"]["blue"]]
                    self.quantum_efficiency_color["red"] = [float(x) for x in sensor_data["quantum_efficiency"]["red"]]
                    self.quantum_efficiency_color["green"] = [float(x) for x in sensor_data["quantum_efficiency"]["green"]]
                    self.quantum_efficiency_color["blue"] = [float(x) for x in sensor_data["quantum_efficiency"]["blue"]]
                    self.quantum_efficiency_wav, self.quantum_efficiency = \
                        self.compute_combined_color_quantum_efficiency()
                    # fig1, ax1 = plt.subplots()
                    # ax1.plot(self.quantum_efficiency_wav_color["red"], self.quantum_efficiency_color["red"])
                    # ax1.plot(self.quantum_efficiency_wav_color["green"], self.quantum_efficiency_color["green"])
                    # ax1.plot(self.quantum_efficiency_wav_color["blue"], self.quantum_efficiency_color["blue"])
                    # plt.show()
                else:
                    return False

                self.dark_noise = float(sensor_data["dark_noise"]) # e- units
                self.dark_current = float(sensor_data["dark_current"]) # e- units
                self.gain = float(sensor_data["gain"])
                logging.debug("Sensor gain: {}".format(self.gain))

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
        sensor_diagonal /= 1000.  # Convert to mm

        coc = sensor_diagonal / 1500.   # common value for 35mm format
        return coc

    def get_quantum_efficiency(self, wave_length):
        """
        Interpolate Quantum efficiency value for a given wavelength
        :param wave_length: Input wavelength
        :return:
        """
        return np.interp(wave_length, self.quantum_efficiency_wav, self.quantum_efficiency)

    def get_quantum_efficiency_color(self, wave_length, color):
        """
        Interpolate Quantum efficiency value for a given wavelength
        :param wave_length: Input wavelength
        :return:
        """
        return np.interp(wave_length, self.quantum_efficiency_wav_color[color], self.quantum_efficiency_color[color])

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
        mono_wav = np.array(self.quantum_efficiency_wav_color["green"], dtype=float)
        red = np.array([np.interp(x, self.quantum_efficiency_wav_color["red"], self.quantum_efficiency_color["red"]) for x in mono_wav], dtype=float)
        green = np.array(self.quantum_efficiency_color["green"], dtype=float)
        blue = np.array([np.interp(x, self.quantum_efficiency_wav_color["blue"], self.quantum_efficiency_color["blue"]) for x in mono_wav], dtype=float)
        # mono_eff = green + red + blue
        # linear conversion to luminance
        # https://www.dynamsoft.com/blog/insights/image-processing/image-processing-101-color-space-conversion/
        # mono_eff = (green + red + blue)/3
        # mono_eff = 0.299*red + 0.587*green + 0.114*blue
        mono_eff = np.max((red,green,blue),axis=0)
        # matplotlib.use('TkAgg')
        # plt.plot(mono_wav, mono_eff)
        # plt.show()
        return mono_wav, mono_eff

    def compute_incident_photons(self, wavelength, exposure_time, irradiance):
        """
        Compute the amount of incident photons for narrowband light
        :param wavelength: wavelength of incident light in [nm]
        :param exposure_time: image shutter time in [s]
        :param irradiance:  Incident Radiance E on sensor surface in [W/m^2]
        :return: Number of incident photons
        """
        exposure_time = exposure_time*math.pow(10, 3) # From s to ms
        irradiance = irradiance * math.pow(10, 2) # from [W/m^2] to [uW/cm^2]
        wavelength = wavelength*math.pow(10, -3) # from nm to um
        pixel_area = self.get_pixel_area('um')
        incident_photons = 50.34 * pixel_area * exposure_time * wavelength * irradiance
        logging.debug("Pixel Area: {} Exposure time: {} Wavelength: {} Irradiance E: {}[W/m2], Photons: {} ".format(pixel_area, exposure_time, wavelength, irradiance, incident_photons))

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

    # Reference: https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf
    # def compute_signal_to_noise_ratio(self, exposure_time, wavelengths, incident_spectrum):
    #     u_a = self.compute_absorbed_photons_broadband(wavelengths, incident_spectrum, exposure_time)
    #     sq_2 = 1/12 # assumes 12bit ADC for machine vision cameras
    #     sd_2 = self.dark_noise**2
    #     k = self.user_gain*self.gain
    #     k_2 = k**2
    #     snr = u_a/math.sqrt(sd_2 + sq_2/k_2 + u_a)
    #     return snr

    # Reference: https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf
    def compute_signal_to_noise_ratio(self, absorbed_photons):
        u_a = absorbed_photons
        sq_2 = 1/12 # assumes 12bit ADC for machine vision cameras with unit integer steps
        sd_2 = self.dark_noise**2
        k_2 = self.gain**2
        snr = u_a/np.sqrt(sd_2 + sq_2/k_2 + u_a)
        # ideal sensor only has shot noise. No dark or quantization noise
        snr_ideal = np.sqrt(u_a)
        return snr, snr_ideal

    def compute_digital_signal(self, exposure_time, wavelength, irradiance):
        """
        Compute the digital signal value
        :param wavelength:  wavelength of incident light in [um]
        :param exposure_time: image shutter time in [ms]
        :param irradiance: Incident Radiance E on sensor surface in [uW/cm^2]
        :return: Mean digital signal
        """
        logging.debug("Compute digital signal narrowband")
        signal = self.user_gain(self.dark_current*exposure_time + self.gain*self.compute_absorbed_photons(wavelength, exposure_time, irradiance))
        return signal/2**16

    def compute_absorbed_photons_broadband_color_map(self, wavelengths, incident_spectrum, exposure_time):
        """
        Compute the number of incident photons for broadband light defined as a spectrum
        :param wavelengths: Array of wavelengths in nm
        :param incident_spectrum: Array with incident light spectrum defined in W/(m2nm)
        :param exposure_time: Exposure time of image in seconds
        :return:
        """
        h = 6.62607004 * math.pow(10, -34)  # Plancks constant (m2kg)/s
        c = 299792458.0  # speed of light in m/s

        # Weight the spectrum with the quantum efficiency curve
        quantum_eff_spectrum = np.zeros((len(wavelengths), 3)) # rgb color channels
        quantum_eff_spectrum[:,0]   = [self.get_quantum_efficiency_color(x, 'red') for x in wavelengths]    # Units: Dimensionless
        quantum_eff_spectrum[:,1] = [self.get_quantum_efficiency_color(x, 'green') for x in wavelengths]    # Units: Dimensionless
        quantum_eff_spectrum[:,2]  = [self.get_quantum_efficiency_color(x, 'blue') for x in wavelengths]    # Units: Dimensionless

        I = np.expand_dims(incident_spectrum, axis=-1)
        I = np.tile(I, (1,1,1,3))
        absorbed_spectrum = np.multiply(I, quantum_eff_spectrum)        # Units: W/(m2nm)

        W = np.expand_dims(wavelengths, axis=-1)
        W = np.tile(W, (1,3))
        lambda_spectrum = np.multiply(absorbed_spectrum, W)  # W/m2

        # Comp incident photons
        # incident_photons_spectrum = np.multiply(incident_spectrum, wavelengths)*exposure_time*self.get_pixel_area('m')/(h*c)
        # incident_photons_total = np.trapz(incident_photons_spectrum, wavelength_m)
        # logging.debug("Max total number of incident photons {}".format(np.max(incident_photons_total)))

        # Absorbed energy
        # absorbed_energy = np.trapz(np.multiply(incident_spectrum, np.multiply(wavelengths, quantum_eff_spectrum)), wavelengths)
        # logging.debug("Absorbed Energy: {}[W/m2]".format(absorbed_energy))

        wavelength_m = np.array(wavelengths)*math.pow(10, -9)
        integral = np.trapz(lambda_spectrum, wavelength_m, axis=2)  # W/m
        photon_density = integral / (h*c)  # Photons/m2s
        photons = photon_density * self.get_pixel_area('m') * exposure_time

        # print(self.get_pixel_area('m'))
        logging.debug("h*c= {}:".format(h*c))
        logging.debug("Pixel Area: {}m2 Exposure time: {}s Wavelengths: {}-{}[nm] Max Integral: {}, Max Photons: {} ".format(self.get_pixel_area('m'), exposure_time, wavelengths[0],wavelengths[-1], np.max(integral), np.max(photons)))

        return photons

    def compute_absorbed_photons_broadband_map(self, wavelengths, incident_spectrum, exposure_time):
        """
        Compute the number of incident photons for broadband light defined as a spectrum
        :param wavelengths: Array of wavelengths in nm
        :param incident_spectrum: Array with incident light spectrum defined in W/(m2nm)
        :param exposure_time: Exposure time of image in seconds
        :return:
        """
        h = 6.62607004 * math.pow(10, -34)  # Plancks constant (m2kg)/s
        c = 299792458.0  # speed of light in m/s

        # Weight the spectrum with the quantum efficiency curve
        quantum_eff_spectrum = [self.get_quantum_efficiency_color(x, 'red') for x in wavelengths]    # Units: Dimensionless
        absorbed_spectrum = np.multiply(quantum_eff_spectrum, incident_spectrum)        # Units: W/(m2nm)

        lambda_spectrum = np.multiply(wavelengths, absorbed_spectrum)  # W/m2

        # Comp incident photons
        incident_photons_spectrum = np.multiply(incident_spectrum, wavelengths)*exposure_time*self.get_pixel_area('m')/(h*c)
        incident_photons_total = np.trapz(incident_photons_spectrum, wavelength_m)
        logging.debug("Max total number of incident photons {}".format(np.max(incident_photons_total)))

        # Absorbed energy
        absorbed_energy = np.trapz(np.multiply(incident_spectrum, np.multiply(wavelengths, quantum_eff_spectrum)), wavelengths)
        logging.debug("Absorbed Energy: {}[W/m2]".format(absorbed_energy))

        wavelength_m = np.array(wavelengths)*math.pow(10, -9)
        integral = np.trapz(lambda_spectrum, wavelength_m)  # W/m
        photon_density = integral / (h*c)  # Photons/m2s
        photons = photon_density * self.get_pixel_area('m') * exposure_time
        # print(self.get_pixel_area('m'))
        logging.debug("h*c= {}:".format(h*c))
        logging.debug("Pixel Area: {}m2 Exposure time: {}s Wavelengths: {}-{}[nm] Max Integral: {}, Max Photons: {} ".format(self.get_pixel_area('m'), exposure_time, wavelengths[0],wavelengths[-1], np.max(integral), np.max(photons)))

        return photons

    def compute_absorbed_photons_broadband(self, wavelengths, incident_spectrum, exposure_time):
        """
        Compute the number of incident photons for broadband light defined as a spectrum
        :param wavelengths: Array of wavelengths in nm
        :param incident_spectrum: Array with incident light spectrum defined in W/(m2nm)
        :param exposure_time: Exposure time of image in seconds
        :return:
        """
        h = 6.62607004 * math.pow(10, -34)  # Plancks constant (m2kg)/s
        c = 299792458.0  # speed of light in m/s

        # Weight the spectrum with the quantum efficiency curve
        quantum_eff_spectrum = [self.get_quantum_efficiency(x) for x in wavelengths]    # Units: Dimensionless
        absorbed_spectrum = np.multiply(quantum_eff_spectrum, incident_spectrum)        # Units: W/(m2nm)

        # Weight the spectrum with the wavelength
        wavelength_m = np.array(wavelengths)*math.pow(10, -9)

        lambda_spectrum = np.multiply(wavelengths, absorbed_spectrum)  # W/m2

        # Comp incident photons
        incident_photons_spectrum = np.multiply(incident_spectrum, wavelengths)*exposure_time*self.get_pixel_area('m')/(h*c)
        incident_photons_total = np.trapz(incident_photons_spectrum, wavelength_m)
        logging.debug("Total number of incident photons {}".format(incident_photons_total))

        # Absorbed energy
        absorbed_energy = np.trapz(np.multiply(incident_spectrum, np.multiply(wavelengths, quantum_eff_spectrum)), wavelengths)
        logging.debug("Absorbed Energy: {}[W/m2]".format(absorbed_energy))

        # plt.plot(wavelengths, incident_photons_spectrum)
        # plt.show()
        # fig, ax1 = plt.subplots()
        # ax1.plot(wavelengths, quantum_eff_spectrum,'b', label="QE")
        # ax1.set_xlabel('Wavelength [nm]')
        # # Make the y-axis label, ticks and tick labels match the line color.
        # ax1.set_ylabel('QE', color='b')
        #
        # ax2 = ax1.twinx()
        # ax2.plot(wavelengths, incident_spectrum, 'r', label="IncSpect")
        # ax2.plot(wavelengths, absorbed_spectrum, 'g', label="AbsSpect")
        # ax2.set_ylabel('mW/(m2nm)', color='r')
        #
        # fig.tight_layout()
        #
        # plt.legend()
        # plt.show()


        integral = np.trapz(lambda_spectrum, wavelength_m)  # W/m
        photon_density = integral / (h*c)  # Photons/m2s
        photons = photon_density * self.get_pixel_area('m') * exposure_time
        # print(self.get_pixel_area('m'))
        logging.debug("h*c= {}:".format(h*c))
        logging.debug("Pixel Area: {}m2 Exposure time: {}s Wavelengths: {}-{}[nm] Integral: {}, Photons: {} ".format(self.get_pixel_area('m'), exposure_time, wavelengths[0],wavelengths[-1], integral, photons))

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
        logging.debug("Gain: {}, Dark Current: {}".format(self.gain,self.dark_current))
        signal = self.user_gain * (self.dark_current*exposure_time + self.gain*photons)
        # assume parameters given with respect to 16bit response, such as provided by FLIR datasheets, and report values in percent exposed
        # signal = signal / 2**12
        signal = signal / 2**16
        return signal, photons

    def compute_digital_signal_broadband_map(self, exposure_time, wavelengths, incident_spectrum):
        """
        Compute the output digital signal
        :param gain: Gain of sensor
        :param exposure_time: Exposure time of image in s
        :param wavelengths: Array of wavelengths in nm
        :param incident_spectrum: Spectrum of incident light in W/(nmm2)
        :return:
        """
        photons = self.compute_absorbed_photons_broadband_map(wavelengths, incident_spectrum, exposure_time)
        logging.debug("Gain: {}, Dark Noise: {}".format(self.gain,self.dark_noise))
        signal = self.user_gain * (self.dark_current*exposure_time + self.gain*photons)
        # assume parameters given with respect to 16bit response, such as provided by FLIR datasheets, and report values in percent exposed
        # signal = signal / 2**12
        signal = signal / 2**16
        return signal, photons

    def compute_digital_signal_broadband_color_map(self, exposure_time, wavelengths, incident_spectrum):
        """
        Compute the output digital signal
        :param gain: Gain of sensor
        :param exposure_time: Exposure time of image in s
        :param wavelengths: Array of wavelengths in nm
        :param incident_spectrum: Spectrum of incident light in W/(nmm2)
        :return:
        """
        photons = self.compute_absorbed_photons_broadband_color_map(wavelengths, incident_spectrum, exposure_time)
        logging.debug("Gain: {}, Dark Noise: {}".format(self.gain,self.dark_noise))
        signal = self.user_gain * (self.dark_current*exposure_time + self.gain*photons)
        # assume gain given as 16bit value and report values in percent exposed
        # assume parameters given with respect to 16bit response, such as provided by FLIR datasheets, and report values in percent exposed
        # signal = signal / 2**12
        signal = signal / 2**16
        return signal, photons

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
        sensor_diag = np.sqrt( self.get_sensor_size('x')**2 + self.get_sensor_size('y')**2) / 1000.
        coc = sensor_diag / 1500.
        return coc


class Lens:
    def __init__(self):
        self.name = None
        self.focal_length = 8.  # In [mm]
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

    # https://www.cs.cmu.edu/afs/cs/academic/class/16823-s16/www/pdfs/appearance-modeling-2.pdf
    def fundamental_radiometric_relation(self, L, N, alfa):
        """
        Fundamental Radiometric relation between scene radiance L and the light Irradiance E reaching the pixel sensor
        :param L: Scene Radiance
        :param N: Lens Aperture
        :param alfa: Off-Axis Angle
        :return: Irradiance reaching the pixel sensor
        """
        E = L*self.lens_aperture_attenuation(N)*self.natural_vignetting(alfa)
        return E

    def fundamental_radiometric_relation_map(self, L, N, cos_alfa):
        """
        Fundamental Radiometric relation between scene radiance L and the light Irradiance E reaching the pixel sensor
        :param L: Scene Radiance
        :param N: Lens Aperture
        :param cos_alfa: Cos of Off-Axis Angle
        :return: Irradiance reaching the pixel sensor
        """
        # https://www.cs.cmu.edu/afs/cs/academic/class/16823-s16/www/pdfs/appearance-modeling-2.pdf
        # https://www.vision-doctor.com/en/optical-errors/vignetting.html
        # only modeling natural vignetting, not artificial vignetting due to lens design
        V = np.expand_dims(cos_alfa**4, axis=-1)
        V = np.tile(V, (1,1,L.shape[-1]))
        E = L*self.lens_aperture_attenuation(N)*V
        return E

    @staticmethod
    def lens_aperture_attenuation(N):
        return (np.pi/4)*((1/N)**2)

    @staticmethod
    def natural_vignetting(alfa):
        # https://www.cs.cmu.edu/afs/cs/academic/class/16823-s16/www/pdfs/appearance-modeling-2.pdf
        # https://www.vision-doctor.com/en/optical-errors/vignetting.html
        # only modeling natural vignetting, not artificial vignetting due to lens design
        return np.cos(alfa)**4

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
        self.transmittance = [t] * len(self.transmittance_wav)
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

        self.port_refraction_idx = 1.5

        self.dome_radius = 0.1
        self.dome_thickness = 0.01

        self.vectorized_dof = np.vectorize(self.get_depth_of_field_width, excluded='self')
        self.vectorized_framerate = np.vectorize(self.compute_framerate, excluded=['self', 'axis', 'overlap'])
        self.vectorized_exposure = np.vectorize(self.max_blur_shutter_time, excluded=['self', 'axis', 'blur'])

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
        fov = 2. * np.arctan2(self.sensor.get_sensor_size(axis)/1000., 2.*self.effective_focal_length)
        # logger.debug("Angular FOV: %f", fov)
        return fov

    def get_fov(self, axis, working_distance):
        """
        Get the size of the area covered by the image
        :param axis: x or y
        :param working_distance: Distance between the camera and the subject
        :return: size of the area covered by the image along the given axis in the same units as working distance
        """
        if self.initialized():
            fov = 2. * working_distance * np.tan(self.get_angular_fov(axis)/2.)
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

    def get_depth_of_field(self, lens_aperture, working_distance):
        if self.housing == 'flat':
            return self.compute_depth_of_field(lens_aperture, working_distance)
        else: # self.housing == 'dome':
            return self.dome_compute_depth_of_field(lens_aperture, working_distance)

    def get_depth_of_field_width(self, lens_aperture, working_distance):
        (n, f) = self.get_depth_of_field(lens_aperture, working_distance)
        return f-n

    def compute_depth_of_field(self, lens_aperture, working_distance):
        f = self.effective_focal_length
        c = self.sensor.get_coc()
        S = working_distance * 1000.
        m = f/S
        N = lens_aperture
        # Resource: http://www.dofmaster.com/equations.html
        H = f**2/(N*c) + working_distance # Hyperfocal distance
        dn = S*(H-f)/(H+S-2*f)          # Near distance of acceptable sharpness 
        if (H-S)/(S*(H-f)) < 1.E-6:     # Check inverse first for infinity
            df = 1.E6
        else:
            df = S*(H-f)/(H-S)              # Far distance of acceptable sharpness
        # dof = (2.*lens_aperture*c*working_distance**2) / (f**2)
        # dof = (2.*N*c*(m+1)) / (m**2 - (N*c/f)**2)
        return (dn/1000., df/1000.)     # Return in m

    def dome_compute_depth_of_field(self, lens_aperture, working_distance):
        # compute camera focus distance for virtual image
        focus_distance = self.dome_world_to_virtual_dist(working_distance)
        (dn_v, df_v) = self.compute_depth_of_field(lens_aperture, focus_distance)
        dn = self.dome_virtual_to_world_dist(dn_v)
        df = self.dome_virtual_to_world_dist(df_v)

        return (dn, df)


    def dome_world_to_virtual_dist(self, dist):
        # nd = index of refraction of dome
        nd = self.port_refraction_idx #index of refraction of port
        d  = self.dome_thickness #assume concentric dome
        r1 = self.dome_radius    #external dome radius 
        r2 = r1 - d              #internal dome radius
        na = 1.0                 #index of refraction of air
        nw = 1.33                #index of refraction of water
        p  = dist                #p=object distance relative to external vertex                   

        f1     = nw*(r1/(nd-nw))        #primary focal length of dome's external surface
        f1p    = f1*nd/nw               #secondary focal length of dome's external surface
        f2p    = nd*(r2/(na-nd))        #primary focal length of dome's internal surface
        f2pp   = f2p*na/nd              #secondary focal length of dome's internal surface
        enovrf = nd/f1p + na/f2pp - (d/f1p)*(na/f2pp)
        f      = nw/enovrf              #primary focal length of the dome
        fpp    = f*na/nw                #secondary focal length of the dome
        a1f    = -f*(1.-d/f2p)          #position of the dome's primary focal plane relative
                                        #to the dome's external vertex (on the dome axis)
        a2fpp  = fpp*(1.-d/f1p)         #position of the dome's secondary focal plane relative
                                        #to the dome's internal vertex (on the dome axis)
        a1h    = f*d/f2p                #position of the dome's primary principal plane relative
                                        #to the dome's external vertex (on the dome axis)
        g      = r1 - a1h               #g=distance from dome principal plane to lens primary
                                        #principal plane. We assume lens primary principal plane
                                        #at center of dome curvature
        a2hpp  = -fpp*d/f1p             #position of the dome's secondary principal plane relative
                                        #to the dome's internal vertex (on the dome axis)
        s      = p+a1h                  #s=object distance relative to primary principal plane
        spp    = na/(nw/f - nw/s)       #image distance relative to secondary principal plane
        ppp    = spp+a2hpp+d            #image distance relative to external vertex
        # m      = -(nw/na)*(spp/s)       #size of image relative to size of object
        # view   = -(spp-g)/(s+g)/m       #view=tangent of lens' effective half-angle of view
                                        #divided by tangent of lens' in-air half-angle
                                        # of view
        return -ppp

    def dome_virtual_to_world_dist(self, dist):
        # nd = index of refraction of dome
        nd  = self.port_refraction_idx #index of refraction of port
        d   = self.dome_thickness #assume concentric dome
        r1  = self.dome_radius    #external dome radius
        r2  = r1 - d              #internal dome radius
        na  = 1.0                 #index of refraction of air
        nw  = 1.33                #index of refraction of water
        ppp = -dist               #ppp=virtual distance relative to external vertex                   

        f1     = nw*(r1/(nd-nw))        #primary focal length of dome's external surface
        f1p    = f1*nd/nw               #secondary focal length of dome's external surface
        f2p    = nd*(r2/(na-nd))        #primary focal length of dome's internal surface
        f2pp   = f2p*na/nd              #secondary focal length of dome's internal surface
        enovrf = nd/f1p + na/f2pp - (d/f1p)*(na/f2pp)
        f      = nw/enovrf              #primary focal length of the dome
        fpp    = f*na/nw                #secondary focal length of the dome
        a1f    = -f*(1.-d/f2p)          #position of the dome's primary focal plane relative
                                        #to the dome's external vertex (on the dome axis)
        a2fpp  = fpp*(1.-d/f1p)         #position of the dome's secondary focal plane relative
                                        #to the dome's internal vertex (on the dome axis)
        a1h    = f*d/f2p                #position of the dome's primary principal plane relative
                                        #to the dome's external vertex (on the dome axis)
        g      = r1 - a1h               #g=distance from dome principal plane to lens primary
                                        #principal plane. We assume lens primary principal plane
                                        #at center of dome curvature
        a2hpp  = -fpp*d/f1p             #position of the dome's secondary principal plane relative
                                        #to the dome's internal vertex (on the dome axis)
        spp    = ppp-a2hpp-d            #image distance relative to secondary principal plane
        if ((1/f - na/(spp*nw)) < 1E-3):
            return 1000.
        s      = 1/(1/f - na/(spp*nw))  #object distance relative to primary principal plane
        p      = s-a1h                  #object distance relative to dome's external vertex

        return p

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
        df = (working_distance + dof/2.) * 1000.  # Convert to mm
        dn = (working_distance - dof/2.) * 1000.  # Convert to mm
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



class Reflectance:
    def __init__(self):
        self.wavelengths = []
        self.reflectance = []

    def load(self):
        pass

def test():
    camera = Camera()
    camera.set_housing('domed')
    camera.lens.init_generic_lens(8., 0.9)
    camera.get_depth_of_field(2.0, 1.0)

if __name__=="__main__":
    test()