import os
import sys
sys.path.append("./src")
cwd = os.getcwd()
print(cwd)
import camera
from spectrometer_analysis import load_csv, filter_duplicates
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import numpy as np
import glob
from scipy.integrate import simps

class CameraResponseExperiments():

    def __init__(self):
        self.camera = camera.Camera()
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../cfg/icx285alM.json")
        # path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../cfg/imx249.json")
        # path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../cfg/imx250C.json")
        self.camera.sensor.load(path)

    def test_camera_response(self, relative_irradiance_path, exposure_time):

        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_irradiance_path)
        wavelength, irradiance = load_csv(filepath)
        w, i = filter_duplicates(wavelength, irradiance)
        idx = np.argmax(i)
        # import pdb
        # pdb.set_trace()
        #plt.plot(w, i)
        #plt.show()
        digital_signal = self.camera.sensor.compute_digital_signal_broadband(exposure_time, w, i)
        # digital_signal = self.camera.sensor.compute_digital_signal(exposure_time, w[idx], i[idx])
        exposure = simps(i, w)*exposure_time  # Wm

        return digital_signal, exposure
#        self.assertAlmostEqual(area, 3.367148, places=4)


if __name__ == '__main__':

    # Set data_dir to data root directory
    # data_dir = "BFS-U3-51S5C/VaryingExposureTime/Set1/"
    # data_dir = "BFS-U3-51S5M/VaryingExposureTime/Set1/"
    # data_dir = "BFLY-PGE-50S5C/VaryingExposureTime/Set3/"
    # data_dir = "BFLY-U323S6M/VaryingExposureTime/Set1/"
    # data_dir = "GT-1380/VaryingExposureTime/Set1"
    data_dir = "GT-1380/Filter500/Set1"

    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), data_dir)
    data_file = os.path.join(data_dir,"data.csv")
    meter_path = os.path.join(data_dir,"LightMeterData")
    
    data_list = []
    with open(data_file, 'r') as file:
        # skip header
        next(file)
        for line in file:
            # expect csv format "Image Name,Shutter Speed (ms),Mean Pixel Value,Light Meter File"
            values = line.strip().split(",")
            meter_file = glob.glob(os.path.join(meter_path, values[3]+"*.csv"))[0]
            value_list = [values[0],float(values[1])*math.pow(10,-3),float(values[2]),meter_file]
            data_list.append(value_list)


    # test_files = ["../test/BFLY-U32356M/LuxCurveTest/LowLux/LightMeterData/BFLY-U32356M-S4_001_02ﾟ_4774K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/LowLux/LightMeterData/BFLY-U32356M-S4_002_02ﾟ_4785K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/LowLux/LightMeterData/BFLY-U32356M-S4_003_02ﾟ_4785K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/LowLux/LightMeterData/BFLY-U32356M-S4_004_02ﾟ_4739K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/LowLux/LightMeterData/BFLY-U32356M-S4_005_02ﾟ_4795K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/LowLux/LightMeterData/BFLY-U32356M-S4_006_02ﾟ_4767K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/LowLux/LightMeterData/BFLY-U32356M-S4_007_02ﾟ_4781K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/LowLux/LightMeterData/BFLY-U32356M-S4_008_02ﾟ_4779K.csv"]
    # exposure_times = np.array([0.049,0.244,0.488,0.732,0.977,1.465,1.953,2.686]) * math.pow(10,-3)
    # measured_response = np.array([3348,7750,13260,18850,24300,35200,45750,60300])

    # test_files = ["../test/BFLY-U32356M/LuxCurveTest/HighLux/LightMeterData/BFLY-U32356M-S5_001_02ﾟ_4778K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/HighLux/LightMeterData/BFLY-U32356M-S5_002_02ﾟ_4744K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/HighLux/LightMeterData/BFLY-U32356M-S5_003_02ﾟ_4740K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/HighLux/LightMeterData/BFLY-U32356M-S5_004_02ﾟ_4729K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/HighLux/LightMeterData/BFLY-U32356M-S5_005_02ﾟ_4717K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/HighLux/LightMeterData/BFLY-U32356M-S5_006_02ﾟ_4743K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/HighLux/LightMeterData/BFLY-U32356M-S5_007_02ﾟ_4706K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/HighLux/LightMeterData/BFLY-U32356M-S5_008_02ﾟ_4746K.csv"]
    # exposure_times = np.array([0.049,0.244,0.488,0.732,0.977,1.465,1.953,2.686]) * math.pow(10,-3)
    # measured_response = np.array([3200,7100,11960,16640,21200,30300,39800,53600])

    # test_files = ["../test/BFLY-U32356M/LuxCurveTest/MidLux/LightMeterData/BFLY-U32356M-S6_001_02ﾟ_4723K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/MidLux/LightMeterData/BFLY-U32356M-S6_002_02ﾟ_4688K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/MidLux/LightMeterData/BFLY-U32356M-S6_003_02ﾟ_4671K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/MidLux/LightMeterData/BFLY-U32356M-S6_004_02ﾟ_4696K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/MidLux/LightMeterData/BFLY-U32356M-S6_005_02ﾟ_4688K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/MidLux/LightMeterData/BFLY-U32356M-S6_006_02ﾟ_4691K.csv",
    #               "../test/BFLY-U32356M/LuxCurveTest/MidLux/LightMeterData/BFLY-U32356M-S6_007_02ﾟ_4701K.csv"]
    # exposure_times = np.array([0.049,0.244,0.488,0.977,1.465,1.953,2.686]) * math.pow(10,-3)
    # measured_response = np.array([3220,7310,12345,22600,32670,42980,57400])

    # test_files = ["../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_001_02ﾟ_5154K.csv",
    #               "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_002_02ﾟ_5158K.csv",
    #               "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_003_02ﾟ_5140K.csv",
    #               "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_004_02ﾟ_5156K.csv",
    #               "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_005_02ﾟ_5156K.csv",
    #               "../test/BFLY-U32356M/VaryingExposureTime/Set1/LightMeterData/BFLY-U32356M-S1_006_02ﾟ_5175K.csv"]
    # exposure_times = np.array([0.019,0.384,0.768,1.152,1.536,1.921]) * math.pow(10,-3)
    # measured_response = np.array([2950,14190,25700,37150,48200,59000])


    experiments = CameraResponseExperiments()
    model_response = []
    exposure_values = []
    measured_response = []
    error_percent = []

    for i in range(len(data_list)):
        file = data_list[i][3]
        exposure_time = data_list[i][1]
        response, exposure = experiments.test_camera_response(file, exposure_time)
        model_response.append(response)
        exposure_values.append(exposure)
        measured_response.append(data_list[i][2])
        error_percent.append(100.0*abs(response - data_list[i][2])/data_list[i][2])


    exposure_values_mw = [value*1000 for value in exposure_values]

    plt.rc('font', family='serif', serif='Times')
    plt.rc('text', usetex=True)
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.rc('axes', labelsize=10)

    width = 3.487
    height = width / 1.618

    fig1, ax1 = plt.subplots()
    fig1.set_size_inches(width, height)
    # fig1.subplots_adjust(left=.16, bottom=.17, right=.99, top=.97)
    ax1.plot(exposure_values_mw, model_response, '--x')
    ax1.plot(exposure_values_mw, measured_response, '-o')
    ax1.legend(['Model', 'Experiments'])
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

    fig1.savefig('exposure_response.png', bbox_inches='tight')
    fig2.savefig('exposure_error.png', bbox_inches='tight')