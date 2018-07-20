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
    main("/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/LightData/LightMeasurements/LEDBENCH_002_02ﾟ_5407K.csv")


