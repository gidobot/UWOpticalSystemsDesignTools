import os
import src.camera
from src.spectrometer_analysis import load_csv, filter_duplicates
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.integrate import simps

class CameraResponseExperiments():

    def __init__(self):
        self.camera = src.camera.Camera()
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../cfg/imx249.json")
        self.camera.sensor.load(path)

    def test_camera_response(self, relative_irradiance_path, exposure_time):

        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_irradiance_path)
        wavelength, irradiance = load_csv(filepath)
        w, i = filter_duplicates(wavelength, irradiance)
        #plt.plot(w, i)
        #plt.show()
        digital_signal = self.camera.sensor.compute_digital_signal_broadband(0.53, exposure_time, w, i)
        exposure = simps(i, w)*exposure_time  # Wm

        return digital_signal, exposure
#        self.assertAlmostEqual(area, 3.367148, places=4)


if __name__ == '__main__':

    test_files = ["../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_001_02ﾟ_5154K.csv",
                  "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_002_02ﾟ_5158K.csv",
                  "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_003_02ﾟ_5140K.csv",
                  "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_004_02ﾟ_5156K.csv",
                  "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_005_02ﾟ_5156K.csv",
                  "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_006_02ﾟ_5175K.csv"]
    exposure_times = np.array([0.019, 0.384, 0.768, 1.152, 1.536, 1.921]) * math.pow(10,-3)
    measured_response = np.array([2950, 14190, 25700, 37150, 48200, 59000])

    experiments = CameraResponseExperiments()
    model_response = []
    exposure_values = []

    for file, exposure_time in zip(test_files, exposure_times):
        response, exposure = experiments.test_camera_response(file, exposure_time)
        model_response.append(response)
        exposure_values.append(exposure)

    plt.plot(exposure_values, model_response, 'x')
    plt.plot(exposure_values, measured_response, 'o')
    plt.legend(['Model', 'Experiments'])
    plt.xlabel('Exposure Value W/m2 *s')
    plt.ylabel('Avg. Sensor Response')
    plt.show()