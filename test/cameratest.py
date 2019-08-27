import os
import sys
sys.path.append("../src")

#cwd = os.getcwd()
#print(cwd)
import camera
import lights
from spectrometer_analysis import load_csv, filter_duplicates
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import numpy as np
import glob
from scipy.integrate import simps

class CameraResponseExperiments():

    def __init__(self, sensorpath, datapath):
        self.camera = camera.Camera()
        sensorpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), sensorpath)
        self.camera.sensor.load(sensorpath)

        self.data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), datapath)

        self.meter_path = os.path.join(self.data_dir, "LightMeterData")

        print(self.data_dir)

    def estimate_camera_response(self, irradiance_path, exposure_time):

        wavelength, irradiance = load_csv(irradiance_path)


        idx = np.argmax(irradiance)
        irradiance_filter = np.zeros(len(irradiance))

        delta = 1
        irradiance_filter[idx-delta:idx+delta+1] = irradiance[idx-delta:idx+delta+1]

        area = np.trapz(irradiance_filter, wavelength)
        #plt.plot(w, irradiance_filter)
        #plt.show()
        digital_signal_broad = self.camera.sensor.compute_digital_signal_broadband(exposure_time, wavelength, irradiance)
        digital_signal_narrow = self.camera.sensor.compute_digital_signal(exposure_time, wavelength[idx], area)
        exposure = simps(irradiance, wavelength)*exposure_time  # Wm

        return digital_signal_narrow, digital_signal_broad, exposure


    def test_lux_values(self, spectrafilename):
        lightspectra = lights.LightSource()

        wavelength, irradiance = load_csv(spectrafilename)

        lightspectra.spectral_wav = wavelength
        lightspectra.spectral_dist = irradiance

        return lightspectra.compute_luminous_flux()

    def process_experiment_set(self):

        data_file = os.path.join(self.data_dir, "data.csv")

        data_list = []
        with open(data_file, 'r') as file:
            # Skip header
            next(file)
            for line in file:
                # expect csv format "Image Name,Shutter Speed (ms),Mean Pixel Value,Light Meter File"
                values = line.strip().split(",")
                meter_file = glob.glob(os.path.join(self.meter_path, values[3] + "*.csv"))[0]
                value_list = [values[0], float(values[1]) * math.pow(10, -3), float(values[2]), meter_file]
                data_list.append(value_list)

        model_response_narrow = []
        model_response_broad = []
        exposure_values = []
        measured_response = []
        error_percent = []

        for i in range(len(data_list)):
            file = data_list[i][3]
            exposure_time = data_list[i][1]
            print("Lux value: {}".format(self.test_lux_values(file)))
            response_broad, response_narrow, exposure = self.estimate_camera_response(file, exposure_time)
            #model_response_narrow.append(response_narrow)
            model_response_broad.append(response_broad*2**4)
            exposure_values.append(exposure)
            measured_response.append(data_list[i][2])
            error_percent.append(100.0 * abs(response_broad - data_list[i][2]) / data_list[i][2])

        exposure_values_mw = [value * 1000 for value in exposure_values]  # Convert x axis to mWs/m2

        plt.rc('xtick', labelsize=10)
        plt.rc('ytick', labelsize=10)
        plt.rc('axes', labelsize=10)

        width = 3.487
        height = width / 1.618

        fig1, ax1 = plt.subplots()
        # fig1.set_size_inches(width, height)
        # fig1.subplots_adjust(left=.16, bottom=.17, right=.99, top=.97)
        #ax1.plot(exposure_values_mw, model_response_narrow, '--x')
        ax1.plot(exposure_values_mw, model_response_broad, '--ro')
        ax1.plot(exposure_values_mw, measured_response, '-o')
        ax1.legend(['Model Broadband', 'Experiments'])
        ax1.set_xlabel('Exposure Value ' + '(mWs' + r'$/$' + 'm^2)')
        ax1.set_ylabel('Avg. Sensor Response')
        ax1.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        fig1.tight_layout()

        fig2, ax2 = plt.subplots()
        fig2.set_size_inches(width, height)
        # fig2.subplots_adjust(left=.12, bottom=.17, right=.99, top=.97)
        ax2.plot(exposure_values_mw[0:], error_percent[0:], '-o')
        ax2.set_xlabel('Exposure Value ' + '(mWs' + r'$/$' + 'm^2)')
        ax2.set_ylabel('Percent Error')
        ax2.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        ax2.set_ylim(ymax=10)
        fig2.tight_layout()

        plt.show()
        print(os.path.join(self.data_dir, 'exposure_response.png'))
        fig1.savefig(os.path.join(self.data_dir, 'exposure_response.png'), bbox_inches='tight')
        fig2.savefig(os.path.join(self.data_dir, 'exposure_error.png'), bbox_inches='tight')


def main():
    # Set data_dir to data root directory
    #sensor_path = "../cfg/imx250M.json"
    #data_dir = "BFS-U3-51S5M/VaryingExposureTime/Set1/"

    #data_dir = "BFS-U3-51S5C/VaryingExposureTime/Set1/"

    # data_dir = "BFLY-PGE-50S5C/VaryingExposureTime/Set3/"


    #data_dir = "BFLY-U323S6M/VaryingExposureTime/Set1/"
    #sensor_path = "../cfg/imx249.json"


    # data_dir = "GT-1380/VaryingExposureTime/Set1"

    #sensor_path = "../cfg/imx178.json"
    #data_dir = "NewTests/BFS-U3-63S4M/ConstantLight/WhiteLight/Set1"

    #sensor_path = "../cfg/imx250M.json"
    #data_dir = "NewTests/BFS-U3-51S5M/ConstantLight/WhiteLight/Set1"
    #data_dir = "OldTests/BFS-U3-51S5M/VaryingExposureTime/Set1"

    sensor_path = "../cfg/imx249.json"
    data_dir = "NewTests/BFLY-U3-23S6M/ConstantLight/SpotLight/Set1"
    #data_dir = "NewTests/BFLY-U3-23S6M/ConstantLight/WhiteLight/Set1"


    experiments = CameraResponseExperiments(sensor_path, data_dir)
    experiments.process_experiment_set()


if __name__ == '__main__':
    main()
