# This Python file uses the following encoding: utf-8

import numpy as np
import scipy.stats
from scipy.integrate import simps
import json

import logging
logger = logging.getLogger(__name__)

class LightSource:
    def __init__(self):
        self.name = None
        self.luminousflux = None
        self.beam_angle = None
        self.spectral_wav = []
        self.spectral_dist = []
        self.initialized = False

        self.photopic_wavelengths = np.arange(370, 780, 10)
        self.photopic_eff = [0.0001, 0.0004, 0.0015, 0.0045, 0.0093, 0.0175, 0.0273, 0.0379, 0.0468, 0.0600,
                        0.0910, 0.1390, 0.2080, 0.3230, 0.5030, 0.7100, 0.8620, 0.9540, 0.9950, 0.9950,
                        0.9520, 0.8700, 0.7570, 0.6310, 0.5030, 0.3810, 0.2650, 0.1750, 0.1070, 0.0610,
                        0.0320, 0.0170, 0.0082, 0.0041, 0.0021, 0.0011, 0.0005, 0.0002, 0.0001, 0.0001,
                        0.0000]

    def compute_beam_area(self, working_distance):
        if self.initialized:
            return np.pi * (np.tan(np.radians(self.beam_angle))*working_distance)**2
        else:
            return 0

    def compute_illuminance(self, working_distance):
        """
        Compute illuminance in lux
        :param working_distance: Distance to the illuminated target in meters
        :return: illuminance in lux
        """
        area = self.compute_beam_area(working_distance)
        illuminance = self.luminousflux / area
        return illuminance

    def get_irradiance_spectrum(self, working_distance):
        """
        Get the spectrum of the light in irradiance units of W/(m2nm)
        :param working_distance: Distance to surface being illuminated
        :return: tuple of spectrum wavelength and corresponding irradiance
        """
        area = self.compute_beam_area(working_distance) # Units: m2
        scale = self.compute_spectral_radiance_scale()  # Units: W/nm
        scale /= area   # Units: W/(nm*m2)

        return self.spectral_wav, scale*self.spectral_dist

    def compute_spectral_radiance_scale(self):
        """
        Compute the scale factor of the radiance curve
        :return: scale factor in Watt
        """


        Emax = self.luminousflux / self.compute_luminous_flux()  # W/nm
        return Emax

    def compute_luminous_flux(self):
        """
        Compute the luminous flux from a light spectrum
        :return:
        """
        wavelengths = np.linspace(np.max([np.min(self.spectral_wav), np.min(self.photopic_wavelengths)]),
                                  np.min([np.max(self.spectral_wav), np.max(self.photopic_wavelengths)]), 100)

        luminosity_integral_func = self.get_spectrum_value(wavelengths) * self.get_photopic_eff(
            wavelengths)  # Dimensionless
        flux = 683.002 * simps(luminosity_integral_func, wavelengths)  # nm

        return flux

    def compute_peak_wavelength(self, T):
        """
        Compute the peak wavelength for a given light temperature in degrees Kelvin using Wiens displacement law
        :param T: Light temperature in K
        :return:  Wavelength in nm
        """
        b = 2.8977729*pow(10, -3)
        wav_length = (b/T) * pow(10, 9)
        return wav_length

    def get_photopic_eff(self, x_values):
        """
        Interpolate the spectral density curve
        Data obtained from http://www.cvrl.org/lumindex.htm (CIE Photopic V(λ) modified by Judd (1951))
        :return: List of tuples. First element in tuple wavelength in nm, second element photopic efficiency
        """
        phot_eff = np.array([np.interp(x, self.photopic_wavelengths, self.photopic_eff) for x in x_values])

        return phot_eff

    def get_spectrum_value(self, x_values):
        """
        Interpolate the relative spectral density curve
        :param x_values: Array of values to interpolate over
        :return:
        """
        spectral_density = np.array([np.interp(x, self.spectral_wav, self.spectral_dist) for x in x_values])

        return spectral_density

    def load(self, file_path):
        """
        Load json with Sensor parameters
        :param filepath: Path to the JSON file
        :return: true if loaded correctly, false otherwise
        """
        with open(file_path) as f:
            light_data = json.load(f)
            try:
                if not light_data["type"] == "light":
                    return False

                self.name = light_data["name"]

                self.beam_angle = float(light_data["beam_angle"])
                self.luminousflux = float(light_data["luminous_flux"])
                self.spectral_wav = np.array([float(x) for x in light_data["wavelengths"]])
                self.spectral_dist = np.array([float(x) for x in light_data["spectral_distribution"]])
                self.initialized = True
            except KeyError as e:
                print("Error parsing json data for light. Key not found:", e)

    def init_generic_led_light(self, luminous_flux, beam_angle):
        self.name = "Generic LED"

        # Led parameters (mean_1, mean_2, std_1, std_2, scale_1, scale_2)
        params = [450.70, 565.43, 11.67,  64.63,  24.49, 119.86]
        m1, m2, s1, s2, k1, k2 = params

        self.spectral_wav = np.linspace(400, 801, 600)
        self.spectral_dist = np.array([k1*scipy.stats.norm.pdf(x, loc=m1, scale=s1) + \
                                k2 * scipy.stats.norm.pdf(x, loc=m2, scale=s2) for x in self.spectral_wav])

        try:
            self.luminousflux = int(luminous_flux)
            self.beam_angle = int(beam_angle)
        except ValueError:
            logger.error("Passed wrong type variable to generic led initialization")

        self.initialized = True
        logger.info("Initialized generic led light with flux %f and beam angle %i", self.luminousflux, self.beam_angle)

    def reset(self):
        self.__init__()

