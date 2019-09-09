from PyQt5 import QtCore, QtGui, QtWidgets
from camera import Camera,  OperationalParameters
from lights import LightSource
from wateratenuationmodel import WaterPropagation
from plotWindows import GraphWindow, PlotWidget

import mainwindow
import sys
import os
import logging
from math import pi
import numpy as np

import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class UnderwaterOpticalCalculatorApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically

        self.model = Model()
        self.init_model()


        self.connections()

        # Init compare camera view
        self.plotWidget = PlotWidget()
        self.plotWidget.plot()

    def init_model(self):
        self.model.scene.altitude = self.altitudeSlider.value()/100
        self.model.scene.overlap = self.overlapSlider.value()/100
        self.model.scene.speed = self.speedSlider.value()/100
        self.model.scene.motion_blur = self.motionBlurSlider.value()
        self.model.scene.depthoffield = self.dofSlider.value()/100
        self.on_orientation_combobox(self.cameraOrientationCombobox.currentIndex())

    def connections(self):
        """
        Sets up the required connections of the
        :return:
        """


        self.actionCompare_Sensors.triggered.connect(lambda: self.modesStack.setCurrentIndex(1))
        self.actionDesigner.triggered.connect(lambda: self.modesStack.setCurrentIndex(0))

        ### Designer Connections ####

        # Lights connections
        self.LightsComboBox.currentIndexChanged.connect(self.on_light_combobox)
        self.beamAngleSlider.valueChanged.connect(self.init_generic_led)
        self.luminousFluxLineEdit.textEdited.connect(self.init_generic_led)
        self.lightsInfoButton.clicked.connect(self.on_lights_info)

        # Water connections
        self.waterTypeComboBox.currentIndexChanged.connect(self.on_water_combobox)
        self.waterModelInfoButton.clicked.connect(self.on_attenuation_info)
        # Lens connections
        self.lensLoadFileButton.clicked.connect(self.on_load_lens)
        self.LensComboBox.currentIndexChanged.connect(self.on_lens_combobox)
        self.focalLengthSlider.valueChanged.connect(self.on_generic_lens_sliders)
        self.transmittanceSlider.valueChanged.connect(self.on_generic_lens_sliders)
        self.lensInfoButton.clicked.connect(self.on_lens_info)

        # Camera connections
        self.cameraLoadFileButton.clicked.connect(self.on_load_camera)
        self.cameraInfoButton.clicked.connect(self.on_camera_info)

        # Scene connections
        self.altitudeSlider.valueChanged.connect(self.on_altitude_slider)
        self.overlapSlider.valueChanged.connect(self.on_overlap_slider)
        self.speedSlider.valueChanged.connect(self.on_speed_slider)
        self.motionBlurSlider.valueChanged.connect(self.on_motionblur_slider)
        self.dofSlider.valueChanged.connect(self.on_depthoffield_slider)
        self.cameraOrientationCombobox.currentIndexChanged.connect(self.on_orientation_combobox)
        self.viewportCombobox.currentIndexChanged.connect(self.on_housing_combobox)

        # Chosen Exposure and Aperture connections
        self.chosenApertureSlider.valueChanged.connect(self.on_aperture_slider)
        self.chosenExposureSlider.valueChanged.connect(self.on_exposure_slider)

        # Plots Buttons
        self.dofPlot.clicked.connect(self.model.plotdof)
        self.frameratePlot.clicked.connect(self.model.plotframerate)
        self.exposurePlot.clicked.connect(self.model.plotmaxexp)

    def on_camera_info(self):
        if self.model.camera.sensor.initialized:
            graph = GraphWindow(self.model.camera.sensor.quantum_efficiency_wav,
                                self.model.camera.sensor.quantum_efficiency,
                                "Wavelength [nm]", "Quantum efficiency", self)
            graph.show()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', "You need to load a camera model before showing its "
                                                         "information.",  QtWidgets.QMessageBox.Ok)

    def on_lights_info(self):

        if self.model.light.initialized:
            graph = GraphWindow(self.model.light.spectral_wav, self.model.light.spectral_dist,
                                "Wavelength [nm]", "Relative Spectum", self)
            graph.show()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', "You need to load a light model before showing its "
                                                         "information.",  QtWidgets.QMessageBox.Ok)

    def on_attenuation_info(self):
        if self.model.water.initialized:
            graph = GraphWindow(self.model.water.jerlov_wavelenths, self.model.water.attenuation_coef,
                                "Wavelength [nm]", "Attenuation  Coefficient", self)
            graph.show()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', "You need to load a water attenuation model before showing its"
                                                         "information.",  QtWidgets.QMessageBox.Ok)

    def on_lens_info(self):
        if self.model.camera.lens.initialized:
            graph = GraphWindow(self.model.camera.lens.transmittance_wav, self.model.camera.lens.transmittance,
                                "Wavelength [nm]", "Transmittance Spectum", self)
            graph.show()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', "You need to load a lens model before showing its "
                                                         "information.",  QtWidgets.QMessageBox.Ok)

    def on_water_combobox(self, index):
        if index == 0:
            # Custom water attenuation profile
            self.model.water.reset()
        elif index == 1:
            # Load Jerlov I profile
            self.model.water.load_jerlovI_profile()
            logging.info("Loaded JerlovI profile")
        elif index == 2:
            self.model.water.load_jerlovII_profile()
            logging.info("Loaded JerlovII profile")
        elif index == 3:
            self.model.water.load_jerlovIII_profile()
            logging.info("Loaded JerlovIII profile")
        elif index == 4:
            self.model.water.load_jerlov1C_profile()
            logging.info("Loaded Jerlov1C profile")
        elif index == 5:
            self.model.water.load_jerlov3C_profile()
            logging.info("Loaded Jerlov3C profile")
        elif index == 6:
            self.model.water.load_jerlov5C_profile()
            logging.info("Loaded Jerlov5C profile")
        elif index == 7:
            self.model.water.load_jerlov7C_profile()
            logging.info("Loaded Jerlov7C profile")
        elif index == 8:
            self.model.water.load_jerlov9C_profile()
            logging.info("Loaded Jerlov9C profile")
        self.updateModel()

    def on_load_lens(self):
        """
        Open a file dialog and load the lens json description file
        :return: None
        """
        lens = self.model.camera.lens

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', QtCore.QDir.homePath())

        if os.path.isfile(filename):
            if lens.load(filename):
                self.lensLoadedFileLabel.setText(lens.name)
                self.focalLengthValueLabel.setNum(lens.focal_length)
                logging.info("Loaded Lens.")
                self.updateModel()

    def on_generic_lens_sliders(self):
        """
        Callback executed when either of the focal length or transmittance sliders for a generic custom lens are
        changed
        :return: None
        """
        f = self.focalLengthSlider.value()
        t = self.transmittanceSlider.value()/100
        self.model.camera.lens.init_generic_lens(f, t)
        logging.info("Created generic lens with focal length %i and transmittance value of %f.",f,t)
        self.updateModel()

    def on_lens_combobox(self, index):
        """
        Callback executed when the lens type combobox is changed.
        :param index: New combobox page index (0=Custom, 1=Generic)
        :return: None
        """
        if index == 1:
            logging.info("Changing to generic lens model")
            f = self.focalLengthSlider.value()
            t = self.transmittanceSlider.value()/100
            self.model.camera.lens.init_generic_lens(f, t)
        elif index == 0:
            logging.info("Changing to custom lens model")
            self.lensLoadedFileLabel.setText("No File Loaded")
            self.focalLengthValueLabel.setNum(0)
            self.model.camera.lens.reset()
        self.updateModel()

    def on_load_camera(self):

        sensor = self.model.camera.sensor

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', QtCore.QDir.homePath())

        if os.path.isfile(filename):
            if sensor.load(filename):
                self.pixelSizeValueLabel.setNum(sensor.pixel_size)
                self.resolutionxValueLabel.setNum(sensor.resolution_x)
                self.resolutionyValueLabel.setNum(sensor.resolution_y)
                self.sensorNameLabel.setText(sensor.name)
                self.cameraLoadedFileLabel.setText(os.path.basename(filename))
                self.updateModel()

                logging.info("Loaded Lens.")

    def on_light_combobox(self, index):
        if index == 0:
            self.model.light.reset()
        elif index == 1:
            # Generic LED light
            self.init_generic_led()
        elif index == 2:
            self.model.light.reset()
        elif index == 3:
            self.model.light.reset()

    def init_generic_led(self):
        """
        Initialize a generic LED. Callback for generic led sliders and LineEdit
        :return:
        """
        self.model.light.init_generic_led_light(self.luminousFluxLineEdit.text(),
                                                    self.beamAngleSlider.value())
        self.updateModel()

    def on_altitude_slider(self):
        self.model.scene.altitude = self.altitudeSlider.value()/100
        logging.info("Modified altitude to %.2f", self.model.scene.altitude)
        self.updateModel()

    def on_overlap_slider(self):
        self.model.scene.overlap = self.overlapSlider.value()/100
        logging.info("Modified overlap to %.2f", self.model.scene.overlap)
        self.updateModel()

    def on_speed_slider(self):
        self.model.scene.speed = self.speedSlider.value()/100
        logging.info("Modified speed to %.2f.", self.model.scene.speed)
        self.updateModel()

    def on_motionblur_slider(self):
        self.model.scene.motion_blur = self.motionBlurSlider.value()
        logging.info("Modified max motion blur to %i.", self.model.scene.motion_blur)
        self.updateModel()

    def on_depthoffield_slider(self):
        self.model.scene.depthoffield = self.dofSlider.value()/100
        logging.info("Modified overlap to %.2f.", self.model.scene.depthoffield)
        self.updateModel()

    def on_orientation_combobox(self, index):
        if index == 0:
            self.model.scene.axis = "x"
        elif index == 1:
            self.model.scene.axis = "y"

        self.updateModel()
        logging.info("Changed camera orientation")

    def on_housing_combobox(self, index):
        if index == 0:
            self.model.camera.set_housing('flat')
        elif index == 1:
            self.model.camera.set_housing('domed')
        else:
            logging.error("Invalid housing option in callback")
        self.updateModel()

    def on_aperture_slider(self):
        self.model.aperture = self.chosenApertureSlider.value() / 10
        logging.info("Modified aperture to %.2f.", self.model.aperture)
        self.updateModel()

    def on_exposure_slider(self):
        self.model.exposure = self.chosenExposureSlider.value()/1000000
        logging.info("Modified exposure to %.2f.", self.model.exposure)
        self.updateModel()

    def updateModel(self):
        self.model.update()
        self.updateUI()

    def updateUI(self):
        self.fovxValueLabel.setText(("%.2f" % self.model.fov_x))
        self.fovyValueLabel.setText("%.2f" % self.model.fov_y)
        self.fovxDegValueLabel.setText("%.2f" % (self.model.fov_x_deg*180/pi))
        self.fovyDegValueLabel.setText("%.2f" % (self.model.fov_y_deg*180/pi))
        self.exposureValueLabel.setText("%.2f" % (self.model.max_exposure*1000))
        self.framerateValueLabel.setText("%.2f" % self.model.framerate)
        self.apertureValueLabel.setText("%.2f" % self.model.min_aperture)
        self.effectiveFocalLengthValueLabel.setText("%.2f" % self.model.eff_focal_length)
        self.avgImgValueValueLabel.setText("%.2f" % self.model.response)
        self.chosenApertureValueLabel.setText("%.2f" % self.model.aperture)
        self.chosenExposureValueLabel.setText("%5.2f" % (self.model.exposure*1000))
        self.chosenApertureSlider.setMinimum(self.model.min_aperture*10)
        self.chosenExposureSlider.setMaximum(self.model.max_exposure*1000000)


class Model:
    def __init__(self):
        self.camera = Camera()
        self.light = LightSource()
        self.scene = OperationalParameters()
        self.water = WaterPropagation()

        self.fov_x = 0
        self.fov_y = 0
        self.fov_x_deg = 0
        self.fov_y_deg = 0
        self.aperture = 2
        self.min_aperture = 1.4
        self.exposure = 0
        self.max_exposure = 1
        self.framerate = 0
        self.eff_focal_length = 0
        self.response = 0

    def update(self):
        logging.info("Updating model")
        if self.camera.lens.initialized:
            self.eff_focal_length = self.camera.effective_focal_length
        else:
            self.eff_focal_length = 0

        if self.camera.initialized():
            self.fov_x = self.camera.get_fov('x', self.scene.altitude)
            self.fov_y = self.camera.get_fov('y', self.scene.altitude)
            self.fov_x_deg = self.camera.get_angular_fov('x')
            self.fov_y_deg = self.camera.get_angular_fov('y')
            self.max_exposure = self.camera.max_blur_shutter_time(self.scene.axis, self.scene.altitude,
                                                              self.scene.speed, self.scene.motion_blur)
            self.framerate = self.camera.compute_framerate(self.scene.axis, self.scene.altitude,
                                                           self.scene.speed, self.scene.overlap)
            self.min_aperture = self.camera.compute_aperture(self.scene.depthoffield, self.scene.altitude)
            if self.min_aperture <= 1:
                self.min_aperture = 1
            elif self.min_aperture >= 64:
                self.min_aperture = 64

        else:
            self.fov_y = 0
            self.fov_x = 0
            self.framerate = 0


        if self.camera.initialized() and self.water.initialized and self.light.initialized:
            logging.info("Updating full image formation model")

            lights_wavelength, lights_irradiance_spectrum = self.light.get_irradiance_spectrum(self.scene.altitude)
            print(np.max(lights_irradiance_spectrum))
            water_attenuation = [self.water.get_attenuation(x, self.scene.altitude) for x in lights_wavelength]
            print(np.max(water_attenuation))
            # TODO: Get reflection value
            reflection = [0.53] * len(water_attenuation)

            lens_transmittance = [self.camera.lens.get_transmittance(x)*
                                  self.camera.lens.lens_aperture_attenuation(self.aperture)
                                  for x in lights_wavelength]
            incident_spectrum = lights_irradiance_spectrum * np.power(water_attenuation, 2) * reflection * lens_transmittance

            self.response = (self.camera.sensor.compute_digital_signal_broadband(self.exposure,
                                                                                lights_wavelength,
                                                                                incident_spectrum)/2**16)*100


    def plotframerate(self):
        speed = np.arange(0.1, 3, 0.1)
        d = np.arange(0.5, 3, 0.1)

        ss, dd = np.meshgrid(speed, d)
        framerate = self.camera.vectorized_framerate(self.scene.axis, dd, ss, self.scene.overlap)

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_title("Frequency")
        ax.set_xlabel("Speed [m/s]")
        ax.set_ylabel("Target Distance [m]")
        ax.set_zlabel("Framerate [Hz}")
        surf = ax.plot_surface(ss, dd, framerate)
        plt.show()

    def plotmaxexp(self):
        speed = np.arange(0.2, 3, 0.1)
        d = np.arange(0.5, 3, 0.1)
        ss, dd = np.meshgrid(speed, d)
        exposure = self.camera.vectorized_exposure(self.scene.axis, dd, ss, self.scene.motion_blur)*1000

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_title("Max exposure")
        ax.set_xlabel("Speed [m/s]")
        ax.set_ylabel("Target Distance [m]")
        ax.set_zlabel("Max exposure [ms]")
        surf = ax.plot_surface(ss, dd, exposure)
        plt.show()

    def plotdof(self):
        N = np.arange(1, 12, 0.1)
        d = np.arange(500, 2000, 100)
        nn, dd = np.meshgrid(N, d)
        res = self.camera.vectorized_dof(nn, dd)/1000


        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_title("Depth of field")
        ax.set_xlabel("Aperture (f#)")
        ax.set_ylabel("Target Distance")
        ax.set_zlabel("Depth of field")
        surf = ax.plot_surface(nn, dd, res)
        plt.show()

def main():
    # logging.basicConfig(filename='/home/eiscar/myapp.log', level=logging.DEBUG, filemode='w')
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info('Started')

    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    app.setWindowIcon(QtGui.QIcon('/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/resources/light_model.png'))
    form = UnderwaterOpticalCalculatorApp()  # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()
    logging.info('Finished')

if __name__=="__main__":
    main()