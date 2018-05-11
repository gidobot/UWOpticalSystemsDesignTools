__author__ = 'eiscar'
import numpy as np
import json


class Sensor:
    def __init__(self):

        self.name = None

        self.resolution_x = None
        self.resolution_y = None

        self.pixel_size = None  # in micro meters

        self.max_shutter_time = None
        self.min_shutter_time = None

        self.quantum_efficiency = [(), ()]  # List of tuples with wavelength,quantum_efficiency

        self.dark_noise = None  # In Electrons

    def load(self, file_path):
        """
        Load json with Sensor parameters
        :param filepath: Path to the JSON file
        :return: true if loaded correctly, false otherwise
        """
        with open(file_path) as f:
            sensor_data = json.load(f)
            try:
                self.name = sensor_data["name"]
                self.resolution_y = sensor_data["resolution_y"]
                self.resolution_x = sensor_data["resolution_x"]
                self.pixel_size = sensor_data["pixel_size"]

                self.max_shutter_time = sensor_data["max_shutter_time"]
                self.min_shutter_time = sensor_data["min_shutter_time"]

                self.quantum_efficiency = zip(sensor_data["quantum_efficiency_wavelengths"],
                                              sensor_data["quantum_efficiency"])

                self.dark_noise = sensor_data["dark_noise"]

            except KeyError as e:
                print("Error parsing json data for sensor. Key not found:",e)

    def get_quantum_efficiency(self, wave_length):
        """
        Interpolate Quantum efficiency value for a
        :param wave_length:
        :return:
        """
        wave_lengths = map(lambda x: x[0], self.quantum_efficiency)
        quantum_efficiencies = map(lambda x: x[1], self.quantum_efficiency)
        return np.interp(wave_length, wave_lengths, quantum_efficiencies)

    def compute_incident_photons(self, wavelength, exposure_time, irradiance):
        """
        Compute the amount of incident photons
        :param wavelength: wavelength of incident light in [um]
        :param exposure_time: image shutter time in [ms]
        :param irradiance:  Incident Radiance E on sensor surface in [uW/cm^2]
        :return: Number of incident photons
        """
        pixel_area = self.pixel_size**2
        incident_photons = 50.34 * pixel_area * exposure_time * wavelength * irradiance
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

    def compute_digital_signal(self, Gain, wavelength, exposure_time, irradiance):
        """
        Compute the digital signal value
        :param Gain: Overall system gain in DN/e- (digits per electron)
        :param wavelength:  wavelength of incident light in [um]
        :param exposure_time: image shutter time in [ms]
        :param irradiance: Incident Radiance E on sensor surface in [uW/cm^2]
        :return: Mean digital signal
        """
        signal = Gain*(self.dark_noise+self.compute_absorbed_photons(wavelength, exposure_time, irradiance))
        return signal

    def get_sensor_size(self, axis):
        """
        Compute the sensor size in micrometers
        :param axis: Sensor axis
        :return: Size along the specified axis im um
        """
        return self.get_resolution(axis) * self.pixel_size

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
        sensor_diag = np.sqrt( self.get_sensor_size('x')**2 + self.get_sensor_size('y')**2) / 1000
        coc = sensor_diag / 1500
        return coc


class Lens:
    def __init__(self):
        self.name = None
        self.focal_length = None  # In [mm]

    def load(self, file_path):
        """
        Load json with lens parameters
        :param filepath: Path to the JSON file
        :return: true if loaded correctly, false otherwise
        """
        with open(file_path) as f:
            lens_data = json.load(f)
            try:
                self.name = lens_data["name"]
                self.focal_length = lens_data["focal_length"]

            except KeyError as e:
                print("Error parsing json data for lens. Key not found:",e)

    def fundamental_radiometric_relation(self, L, N, alfa):
        """
        Fundamental Radiometric relation between scene radiance L and the light Irradiance E reaching the pixel sensor
        :param L: Scene Radiance
        :param N: Lens Aperture
        :param alfa: Off-Axis Angle
        :return: Irradiance reaching the pixel sensor
        """
        E = L*(np.pi/4)*((1/N)**2)*np.cos(alfa)**4
        return E

    def get_aperture_diameter(self, N):
        """
        Compute the lens aperture diameter
        :param N: Lens aperture number
        :return: Diameter of lens aperture in mm
        """
        d = self.focal_length/N
        return d


class Camera:
    def __init__(self):
        self.sensor = Sensor()
        self.lens = Lens()

    def get_angular_fov(self, axis):
        """
        Get the angular field of view in radians on the specified axis
        :param axis: Either x or y
        :return: FOV in radians
        """
        fov = np.arctan2(self.sensor.get_sensor_size(axis)/1000, 2*self.lens.focal_length)
        return fov

    def get_horizontal_fov(self,axis, working_distance):
        """
        Get the size of the area covered by the image
        :param axis: x or y
        :param working_distance: Distance between the camera and the subject, in mm
        :return: size of the area covered by the image along the given axis
        """
        horizontal_fov = 2 * working_distance * np.tan(self.get_angular_fov(axis)/2)
        return horizontal_fov

    def max_blur_shutter_time(self,axis, working_distance, camera_speed, blur):
        """
        Compute the maximum exposure time to ensure motion smaller than the specified value
        :param axis: Axis (x or y) along which the camera is moving
        :param working_distance: Distance between the camera and the subject, in mm
        :param camera_speed: Speed of the camera movement along the specified axis in mm/s
        :param blur: Maximum allowable motion blur in pixels
        :return:
        """
        pixel_res = self.sensor.get_resolution(axis)/self.get_horizontal_fov(axis, working_distance)
        pixel_speed = camera_speed * pixel_res
        max_shutter_time = blur/pixel_speed
        return max_shutter_time

    def compute_depth_of_field(self, lens_aperture, focus_distance):
        f = self.lens.focal_length
        c = self.sensor.get_circle_of_confusion()
        dof = (2*lens_aperture*c*f**2*focus_distance**2) / (f**4-lens_aperture**2*c**2*focus_distance**2)
        return dof


class LightSource:
    def __init__(self):
        pass

class WaterPropagation:
    def __init__(self):
        pass

class Application:
    def __init__(self):
        pass


if __name__ == "__main__":
    image_sensor = Sensor()
    image_sensor.load("/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/cfg/database.json")
    print(list(image_sensor.quantum_efficiency))
