__author__ = 'eiscar'
import csv
import matplotlib.pyplot as plt
import scipy.stats
import scipy.optimize
import numpy as np
import os
import lights as lg
import wateratenuationmodel as wt
import camera as cam

def load_csv(filepath):
    wavelength = []
    irradiance = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=',',)
        for row in reader:
            try:
                if "Spectral Data" in row[0]:
                    wavelength.append(int(row[0][13:17]))
                    irradiance.append(float(row[1]))
            except:
                pass

    return (wavelength, irradiance)

def plot_spectrum(wavelength, irradiance):
    plt.plot(wavelength, irradiance)
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Irradiance [W/m2]")
    plt.show()

def filter_duplicates(x,y):
    seen = {}
    x_o = []
    y_o = []
    for x_element, y_element in zip(x, y):
        #print(x_element)
        if x_element not in seen:
            seen[x_element] = 1
            x_o.append(x_element)
            y_o.append(y_element)

    y_o = [y for _,y in sorted(zip(x_o, y_o))]
    x_o.sort()
    return x_o, y_o

def normalize(y):
    return y/np.max(y)

def fit_spectrum(wavelength, spectrum):
    #params = [460, 560, 20, 50, 2.5, 2.5]
    params = [450, 560, 20, 50, 7, 12]
    fitted_params, _ = scipy.optimize.curve_fit(bi_norm, wavelength, spectrum, p0=params,
                                                bounds=([430, 530, 5, 40, 0.5, 0.5],
                                                        [470, 600, 40, 120, np.inf, np.inf]))
    print(fitted_params)
    alt_params = [450, 560, 20, 50, 7, 12]
    plt.plot(wavelength, spectrum, 'b')
    xx = np.linspace(np.min(wavelength), np.max(wavelength), 1000)
    plt.plot(xx, bi_norm(xx, *fitted_params))
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Irradiance [W/m2]")
    plt.show()

def bi_norm(x, *args):
    m1, m2, s1, s2, k1, k2 = args
    ret = k1*scipy.stats.norm.pdf(x, loc=m1, scale=s1) + k2*scipy.stats.norm.pdf(x, loc=m2, scale=s2)

    return ret

def plot_light_spectrum_comparison():
    """
    This function creates a plot comparing the normalized light spectra of different light sources
    :return: None
    """
    led_file = "/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/LightData/LightMeasurements/LEDBENCH_002_02ﾟ_5407K.csv"
    fluorescent_file = "/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/test/GeneralLightTests/FlourescentTube/FLUORESCEND-TUBE_001_02ﾟ_3328K.csv"
    sun_file = "/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/test/GeneralLightTests/Sun/SUN_001_02ﾟ_5575K.csv"

    led_wave, led_spectrum = filter_duplicates(*load_csv(led_file))
    led_spectrum = np.divide(led_spectrum, np.max(led_spectrum))
    fluorescent_wave, fluorescent_spectrum = filter_duplicates(*load_csv(fluorescent_file))
    fluorescent_spectrum = np.divide(fluorescent_spectrum, np.max(fluorescent_spectrum))
    sun_wave, sun_spectrum = filter_duplicates(*load_csv(sun_file))
    sun_spectrum = np.divide(sun_spectrum, np.max(sun_spectrum))
    plt.plot(led_wave, led_spectrum, 'r')
    plt.plot(fluorescent_wave, fluorescent_spectrum, 'g')
    plt.plot(sun_wave, sun_spectrum, 'b')
    plt.ylim(0, 1.5)
    plt.xlabel("Wavelength [nm]", fontsize=24)
    plt.ylabel("Relative Spectrum", fontsize=24)
    plt.legend(['Led ', 'Fluorescent ', 'Sunlight'], loc=1, fontsize=14, ncol=3)
    plt.tight_layout()
    plt.show()


def get_global_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def analyze_complete_pipeline():

    # Define Spectrogram files
    ambient_file = "../test/BFLY-U32356M/CompletePipeline/OneMeterDist/LightmeterData/EXP-TOTAL_002_02ﾟ_Under.csv"
    board_file1 = "../test/BFLY-U32356M/CompletePipeline/OneMeterDist/LightmeterData/EXP-TOTAL_003_02ﾟ_5384K.csv"
    board_file2 = "../test/BFLY-U32356M/CompletePipeline/OneMeterDist/LightmeterData/EXP-TOTAL_004_02ﾟ_5522K.csv"
    board_file3 = "../test/BFLY-U32356M/CompletePipeline/OneMeterDist/LightmeterData/EXP-TOTAL_005_02ﾟ_5553K.csv"
    board_file4 = "../test/BFLY-U32356M/CompletePipeline/OneMeterDist/LightmeterData/EXP-TOTAL_006_02ﾟ_5474K.csv"

    camera_file1 = "../test/BFLY-U32356M/CompletePipeline/OneMeterDist/LightmeterData/EXP-TOTAL_007_02ﾟ_5797K.csv"
    camera_file2 = "../test/BFLY-U32356M/CompletePipeline/OneMeterDist/LightmeterData/EXP-TOTAL_008_02ﾟ_5857K.csv"
    camera_file3 = "../test/BFLY-U32356M/CompletePipeline/OneMeterDist/LightmeterData/EXP-TOTAL_009_02ﾟ_5882K.csv"
    camera_file4 = "../test/BFLY-U32356M/CompletePipeline/OneMeterDist/LightmeterData/EXP-TOTAL_010_02ﾟ_5809K.csv"

    # Experimental exposure values and image responses
    exposure_times = 0.000049 * np.array([2600, 2400, 2200, 2000, 1800, 1600, 1400, 1200, 1000, 800, 600, 400, 300, 200, 100, 50])
    sensor_response = [65407, 65385, 62600, 53700, 48500, 43200, 38000, 32600, 27300, 21800, 16300, 10900, 8100, 5400,
                       2700, 1350]
    sensor_description_file = "../cfg/imx249.json"

    # Load Spectrogram data
    ambient_wave, ambient_spectrum = filter_duplicates(*load_csv(ambient_file))
    board1_wave, board1_spectrum = filter_duplicates(*load_csv(board_file1))
    board2_wave, board2_spectrum = filter_duplicates(*load_csv(board_file2))
    board3_wave, board3_spectrum = filter_duplicates(*load_csv(board_file3))
    board4_wave, board4_spectrum = filter_duplicates(*load_csv(board_file4))
    board_spectrum_average = (np.array(board1_spectrum) + np.array(board2_spectrum) +np.array(board3_spectrum)+ np.array(board4_spectrum)) / 4

    camera1_wave, camera1_spectrum = filter_duplicates(*load_csv(camera_file1))
    camera2_wave, camera2_spectrum = filter_duplicates(*load_csv(camera_file2))
    camera3_wave, camera3_spectrum = filter_duplicates(*load_csv(camera_file3))
    camera4_wave, camera4_spectrum = filter_duplicates(*load_csv(camera_file4))
    camera_spectrum_average = (np.array(camera1_spectrum) + np.array(camera2_spectrum) +np.array(camera3_spectrum)+ np.array(camera4_spectrum)) / 4

    # Create Light model
    light = lg.LightSource()
    light.init_generic_led_light(0.75*2500, 45)
    lights_wavelength, lights_irradiance_spectrum = light.get_irradiance_spectrum(1)

    # Get water attenuation model and compute light on board
    water = wt.WaterPropagation()
    water.load_jerlovIII_profile()
    water_attenuation = [water.get_attenuation(x, 1) for x in lights_wavelength]
    model_board_spectrum = np.multiply(lights_irradiance_spectrum, water_attenuation)

    # Compute reflected spectrum
    object_reflectivity = len(lights_wavelength) * [0.05]
    model_board_reflection = np.multiply(model_board_spectrum, np.array(object_reflectivity))

    # Get camera incident spectrum
    model_camera_spectrum = np.multiply(model_board_reflection, water_attenuation)

    # Create camera
    camera = cam.Camera()
    camera.sensor.load(get_global_path(sensor_description_file))

    model_camera_response = []
    for exposure_time in exposure_times:
        model_camera_response.append(camera.sensor.compute_digital_signal_broadband(
            0.53, exposure_time, lights_wavelength, model_camera_spectrum))

    # Generate plots
    plt.figure(1)
    plt.subplot(331)
    plt.plot(board1_wave, board1_spectrum, 'b', board2_wave, board2_spectrum, 'k', board3_wave, board3_spectrum, 'c',
             board4_wave, board4_spectrum, 'r', board4_wave, board_spectrum_average, 'g')
    plt.title('Board Incident Spectrum')
    plt.xlabel('Wavelength')
    plt.ylabel('Radiance W/(m2nm)')
    plt.legend(['M1', 'M2', 'M3', 'M4', 'Average'])

    plt.subplot(334)
    plt.plot(camera1_wave,camera1_spectrum, 'b', camera2_wave, camera2_spectrum, 'k', camera3_wave, camera3_spectrum, 'c',
             camera4_wave,camera4_spectrum, 'r',)
    plt.xlabel('Wavelength')
    plt.legend(['M1', 'M2', 'M3', 'M4'])
    plt.title('Camera Incident Spectrum')
    plt.ylabel('Radiance W/(m2nm)')

    plt.subplot(333)
    plt.plot(lights_wavelength, water_attenuation)
    plt.xlabel('Wavelength')
    plt.ylabel('Attenuation')
    plt.title('Attenuation factor')

    plt.subplot(332)
    plt.plot(lights_wavelength, model_board_spectrum, 'r', board4_wave, board_spectrum_average, 'g')
    plt.title('Model Board Incident Spectrum')
    plt.xlabel('Wavelength')
    plt.ylabel('Radiance W/(m2nm)')
    plt.legend(['Model', 'Measured Average'])

    plt.subplot(335)
    plt.plot(lights_wavelength, model_camera_spectrum,'r', camera4_wave, camera_spectrum_average, 'g')
    plt.title('Model Camera Incident Spectrum')
    plt.legend(['Model', 'Measured Average'])
    plt.xlabel('Wavelength')
    plt.ylabel('Radiance W/(m2nm)')

    plt.subplot(336)
    plt.plot(lights_wavelength, object_reflectivity)
    plt.title('Object reflectivity')
    plt.legend('Reflectivity')
    plt.xlabel('Wavelength')
    plt.ylabel('Reflectivity')

    plt.subplot(338)
    plt.plot(exposure_times, model_camera_response,'r', exposure_times, sensor_response,'g')
    plt.xlabel('Exposure [s]')
    plt.ylabel('Camera response [bits]')
    plt.legend(['Model response', 'Measured response'])
    plt.title('Camera Response')
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    #plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)

    plt.figure(2)
    plt.plot(exposure_times, model_camera_response,'r', exposure_times, sensor_response,'g')
    plt.xlabel('Exposure [s]', fontsize=24)
    plt.ylabel('Camera response ', fontsize=24)
    plt.legend(['Model response', 'Measured response'], fontsize=14)
    plt.title('Camera Response', fontsize=24)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.tight_layout()
    plt.show()

def main(filepath):
    wavelength, irradiance = load_csv(filepath)
    w, i = filter_duplicates(wavelength, irradiance)
    i = normalize(i)
#    plot_spectrum(w, i)
    fit_spectrum(w, i)

if __name__=="__main__":
    #main("/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/LightData/LightMeasurements/LEDARRAY_001_02ﾟ_6471K.csv")
    #main("/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/LightData/LightMeasurements/LEDARRAY_002_02ﾟ_6478K.csv")

    #main("/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/LightData/LightMeasurements/LEDFIX2500DX100_001_02ﾟ_5273K.csv")
    #main("/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/LightData/LightMeasurements/LEDBENCH_001_02ﾟ_5416K.csv")
    #main("/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/LightData/LightMeasurements/LEDBENCH_002_02ﾟ_5407K.csv")
    #plot_light_spectrum_comparison()
    analyze_complete_pipeline()
