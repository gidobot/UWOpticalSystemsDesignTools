__author__ = 'eiscar'
import csv
import matplotlib.pyplot as plt
import scipy.stats
import scipy.optimize
import numpy as np

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
    plot_light_spectrum_comparison()

