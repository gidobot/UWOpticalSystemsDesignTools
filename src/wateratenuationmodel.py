import numpy as np
import json
import math

import logging
logger = logging.getLogger(__name__)


class WaterPropagation:
    def __init__(self):
        # Jerlov Profile data obtained from "Inherent optical properties of Jerlov water types  ny
        # MICHAEL G. SOLONENKO AND CURTIS D. M0BLEY"

        self.attenuation_coef = []
        self.initialized = False

        self.jerlov_wavelenths = [300, 310, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700]

    def get_attenuation(self, wavelength, distance):

        if not np.all(np.diff(self.jerlov_wavelenths) > 0):
            logger.error("Input Array not monotonically increasing for interpolation")
            raise ValueError("Input Array not monotonically increasing for interpolation")

        if wavelength < self.jerlov_wavelenths[0] or wavelength > self.jerlov_wavelenths[-1]:
            logger.info("Requested value out of interpolation bounds")
        b = np.interp(wavelength, self.jerlov_wavelenths, self.attenuation_coef)
        return math.exp(b*distance)

    def load_jerlovI_profile(self):

        self.attenuation_coef = [0.173, 0.151, 0.0619, 0.0377, 0.0284, 0.0222, 0.0192, 0.0182, 0.0284, 0.0398, 0.0598,
                            0.0834, 0.163, 0.301, 0.357, 0.416, 0.528]

        self.initialized = True

    def load_jerlovII_profile(self):

        self.attenuation_coef = [0.439, 0.371, 0.174, 0.116, 0.0846, 0.0672, 0.0619, 0.0619, 0.0672, 0.0780, 0.0998, 0.134,
                            0.223, 0.342, 0.393, 0.454, 0.580]

        self.initialized = True

    def load_jerlovIII_profile(self):

        self.attenuation_coef = [0.837, 0.693, 0.342, 0.236, 0.174, 0.139, 0.122, 0.117, 0.116, 0.122, 0.145, 0.145, 0.192,
                            0.288, 0.386, 0.431, 0.494, 0.616]

        self.initialized = True

    def load_jerlov1C_profile(self):

        self.attenuation_coef = [3.244, 2.577, 1.204, 0.616, 0.371, 0.236, 0.174, 0.134, 0.119, 0.122, 0.145, 0.192, 0.288,
                            0.386, 0.431, 0.494, 0.616]

        self.initialized = True

    def load_jerlov3C_profile(self):

        self.attenuation_coef = [5.705, 4.507, 1.772, 1.079, 0.635, 0.416, 0.288, 0.223, 0.198, 0.198, 0.211, 0.248, 0.342,
                            0.431, 0.478, 5.705, 4.507 ]

        self.initialized = True

    def load_jerlov5C_profile(self):

        self.attenuation_coef = [6.42, 5.33, 2.43, 1.56, 1.02, 0.693, 0.511, 0.400, 0.342, 0.315, 0.329, 0.357, 6.42, 5.33,
                            2.43, 1.56, 1.02]

        self.initialized = True

    def load_jerlov7C_profile(self):

        self.attenuation_coef = [6.92, 5.91, 3.00, 2.12, 1.51, 1.14, 0.868, 0.693, 0.580, 0.494, 0.462, 0.462, 0.478, 0.545,
                            0.635, 0.777, 0.916]

        self.initialized = True

    def load_jerlov9C_profile(self):

        self.attenuation_coef = [8.11, 7.01, 4.30, 3.06, 2.41, 1.90, 1.56, 1.24, 1.00, 0.777, 0.635, 0.580, 0.598, 0.654,
                            0.755, 0.916, 1.11]

        self.initialized = True
