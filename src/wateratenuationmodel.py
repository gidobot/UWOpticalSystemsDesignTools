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

        if (wavelength < self.jerlov_wavelenths[0]) or (wavelength > self.jerlov_wavelenths[-1]):
            logger.info("Requested value out of interpolation bounds")
        b = np.interp(wavelength, self.jerlov_wavelenths, self.attenuation_coef)
        return math.exp(-b*distance)

    def load_jerlovI_profile(self):

        Kd = [0.173, 0.151, 0.0619, 0.0377, 0.0284, 0.0222, 0.0192, 0.0182, 0.0284, 0.0398, 0.0598,
                            0.0834, 0.163, 0.301, 0.357, 0.416, 0.528]
        a = [0.163, 0.134, 0.048, 0.030, 0.022, 0.017, 0.018, 0.019, 0.026, 0.046, 0.062, 0.082, 0.228, 0.295,
             0.334, 0.434, 0.582]
        b = [2.08E-02, 1.81E-02, 1.08E-02, 8.11E-03, 6.20E-03, 4.82E-03, 3.81E-03, 3.06E-03, 2.49E-03, 2.05E-03,
             1.70E-03, 1.43E-03, 1.22E-03, 1.04E-03, 8.99E-04, 7.82E-04, 6.85E-04]
        self.attenuation_coef = np.array(a) + np.array(b)
        self.initialized = True

    def load_jerlovII_profile(self):

        Kd = [0.439, 0.371, 0.174, 0.116, 0.0846, 0.0672, 0.0619, 0.0619, 0.0672, 0.0780, 0.0998, 0.134,
                            0.223, 0.342, 0.393, 0.454, 0.580]
        a = [0.343,0.273,0.095,0.0540,0.0355,0.0257,0.0241,0.0228,0.0288,0.0469,0.0622,0.0821,0.228,0.296,0.334,0.436, 0.582]
        b = [1.014,0.957,0.776,0.689,0.616,0.555,0.504,0.459,0.421,0.387,0.358,0.332,0.309,0.288,0.270,0.253,0.238]
        self.attenuation_coef = np.array(a) + np.array(b)
        self.initialized = True

    def load_jerlovIII_profile(self):

        Kd = [0.837, 0.693, 0.342, 0.236, 0.174, 0.139, 0.122, 0.117, 0.116, 0.122, 0.145, 0.145, 0.192,
                            0.288, 0.386, 0.431, 0.494, 0.616]
        a = [0.568,0.452,0.164,0.094,0.0615,0.0449,0.0388,0.0335,0.0358,0.0507,0.0646,0.0838,0.229,0.297,0.336,0.439,0.583]
        b = [2.76,2.61,2.12,1.88,1.69,1.52,1.38,1.26,1.152,1.06,0.980,0.908,0.845,0.788,0.737,0.692,0.650]
        self.attenuation_coef = np.array(a) + np.array(b)

        self.initialized = True

    def load_jerlov1C_profile(self):

        Kd = [3.244, 2.577, 1.204, 0.616, 0.371, 0.236, 0.174, 0.134, 0.119, 0.122, 0.145, 0.192, 0.288,
                            0.386, 0.431, 0.494, 0.616]
        a = [2.686,2.083,0.721,0.386,0.227,0.147,0.105,0.077,0.064,0.068,0.076,0.092,0.236,0.304,0.344,0.455,0.586]
        b = [1.037,0.979,0.793,0.704,0.630,0.567,0.514,0.469,0.429,0.395,0.365,0.338,0.314,0.293,0.274,0.257,0.242]
        self.attenuation_coef = np.array(a) + np.array(b)

        self.initialized = True

    def load_jerlov3C_profile(self):

        Kd = [5.705, 4.507, 1.772, 1.079, 0.635, 0.416, 0.288, 0.223, 0.198, 0.198, 0.211, 0.248, 0.342,
                            0.431, 0.478, 5.705, 4.507 ]
        a = [4.733,3.668,1.287,0.685,0.388,0.236,0.154,0.105,0.081,0.078,0.082,0.095,0.239,0.307,0.346,4.733,3.668]
        b = [3.00,2.83,2.30,2.04,1.83,1.65,1.50,1.36,1.25,1.15,1.06,0.985,0.916,0.855,0.800,3.00,2.83]
        self.attenuation_coef = np.array(a) + np.array(b)
        self.initialized = True

    def load_jerlov5C_profile(self):

        Kd = [6.42, 5.33, 2.43, 1.56, 1.02, 0.693, 0.511, 0.400, 0.342, 0.315, 0.329, 0.357, 6.42, 5.33,
                            2.43, 1.56, 1.02]
        a =[5.36,4.34,1.78,1.05,0.660,0.437,0.297,0.204,0.151,0.127,0.117,0.119,5.36,4.34,1.78,1.05,0.660]
        b = [3.73,3.53,2.87,2.55,2.28,2.06,1.87,1.71,1.56,1.44,1.33,1.23,3.73,3.53,2.87,2.55,2.28]
        self.attenuation_coef = np.array(a) + np.array(b)
        self.initialized = True

    def load_jerlov7C_profile(self):

        Kd = [6.92, 5.91, 3.00, 2.12, 1.51, 1.14, 0.868, 0.693, 0.580, 0.494, 0.462, 0.462, 0.478, 0.545,
                            0.635, 0.777, 0.916]
        a = [5.11,4.40,2.17,1.45,1.03,0.753,0.542,0.388,0.290,0.233,0.195,0.175,0.301,0.367,0.403,0.559,0.621]
        b = [6.56,6.20,5.04,4.49,4.02,3.63,3.30,3.01,2.76,2.54,2.35,2.18,2.03,1.89,1.77,1.66,1.56]
        self.attenuation_coef = np.array(a) + np.array(b)

        self.initialized = True

    def load_jerlov9C_profile(self):

        Kd = [8.11, 7.01, 4.30, 3.06, 2.41, 1.90, 1.56, 1.24, 1.00, 0.777, 0.635, 0.580, 0.598, 0.654,
                            0.755, 0.916, 1.11]
        a = [5.466,4.900,2.856,2.103,1.613,1.242,0.943,0.709,0.543,0.430,0.348,0.291,0.390,0.436,0.456,0.604,0.651]
        b = [8.76,8.28,6.73,5.99,5.36,4.84,4.39,4.01,3.67,3.38,3.12,2.89,2.69,2.51,2.35,2.20,2.07]
        self.attenuation_coef = np.array(a) + np.array(b)
        self.initialized = True
