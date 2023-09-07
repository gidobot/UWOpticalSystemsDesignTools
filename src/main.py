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
import glob

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
        self.on_altitude_slider()
        self.on_overlap_slider()
        self.on_speed_slider()
        self.on_motionblur_slider()
        self.on_orientation_combobox(self.cameraOrientationCombobox.currentIndex())
        self.on_lens_combobox(self.LensComboBox.currentIndex())
        self.on_light_combobox(self.LightsComboBox.currentIndex())
        self.on_dome_radius_change()
        self.on_dome_thickness_change()

        for key in self.model.scene.bottom_type_dict:
            self.bottomTypeCombo.addItem(key)
        index = self.bottomTypeCombo.findText('Benthic Average')
        if index >= 0:
            self.bottomTypeCombo.setCurrentIndex(index)

        sensor_file_list = glob.glob("../cfg/sensors/*.json")
        self.sensor_dict = {}
        for file in sensor_file_list:
            name = os.path.splitext(os.path.split(file)[1])[0]
            self.sensor_dict[name] = file
            self.cameraComboBox.addItem(name)

        # default is flat viewport
        self.domeRadiusLabel.hide()
        self.domeRadiusLineEdit.hide()
        self.domeRadiusUnitsLabel.hide()
        self.domeThicknessLabel.hide()
        self.domeThicknessLineEdit.hide()
        self.domeThicknessUnitsLabel.hide()
        self.domeDistanceLabel.hide()
        self.domeDistanceValueLabel.hide()
        self.domeDistanceUnitsLabel.hide()

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
        self.beamAngleLineEdit.editingFinished.connect(self.on_beam_angle_change)
        self.luminousFluxLineEdit.editingFinished.connect(self.init_generic_led)
        self.lightsInfoButton.clicked.connect(self.on_lights_info)

        # Water connections
        self.waterTypeComboBox.currentIndexChanged.connect(self.on_water_combobox)
        self.waterModelInfoButton.clicked.connect(self.on_attenuation_info)
        # Lens connections
        self.lensLoadFileButton.clicked.connect(self.on_load_lens)
        self.LensComboBox.currentIndexChanged.connect(self.on_lens_combobox)
        self.focalLengthSlider.valueChanged.connect(self.on_generic_lens_sliders)
        self.focalLengthLineEdit.editingFinished.connect(self.on_focal_length_change)
        self.transmittanceSlider.valueChanged.connect(self.on_generic_lens_sliders)
        self.transmittanceLineEdit.editingFinished.connect(self.on_transmittance_change)
        self.lensInfoButton.clicked.connect(self.on_lens_info)

        # Camera connections
        self.cameraLoadFileButton.clicked.connect(self.on_load_camera)
        self.cameraInfoButton.clicked.connect(self.on_camera_info)
        self.cameraComboBox.currentIndexChanged.connect(self.on_camera_combobox)

        # Scene connections
        self.altitudeSlider.valueChanged.connect(self.on_altitude_slider)
        self.altitudeLineEdit.editingFinished.connect(self.on_altitude_change)
        self.overlapSlider.valueChanged.connect(self.on_overlap_slider)
        self.overlapLineEdit.editingFinished.connect(self.on_overlap_change)
        self.speedSlider.valueChanged.connect(self.on_speed_slider)
        self.speedLineEdit.editingFinished.connect(self.on_speed_change)
        self.motionBlurSlider.valueChanged.connect(self.on_motionblur_slider)
        self.motionBlurLineEdit.editingFinished.connect(self.on_motionblur_change)
        self.cameraOrientationCombobox.currentIndexChanged.connect(self.on_orientation_combobox)
        self.viewportCombobox.currentIndexChanged.connect(self.on_housing_combobox)
        self.bottomTypeCombo.currentIndexChanged.connect(self.on_bottom_combo)

        # Chosen Exposure and Aperture connections
        self.chosenApertureSlider.valueChanged.connect(self.on_aperture_slider)
        self.apertureLineEdit.editingFinished.connect(self.on_aperture_change)
        self.chosenExposureSlider.valueChanged.connect(self.on_exposure_slider)
        self.chosenExposureLineEdit.editingFinished.connect(self.on_exposure_change)

        # Gain connections
        self.gainSlider.valueChanged.connect(self.on_gain_slider)
        self.gainLineEdit.editingFinished.connect(self.on_gain_change)

        # Dome housing connections
        self.domeRadiusLineEdit.editingFinished.connect(self.on_dome_radius_change)
        self.domeThicknessLineEdit.editingFinished.connect(self.on_dome_thickness_change)

        # Port refractive index connection
        self.refractionLineEdit.editingFinished.connect(self.on_refractive_change)

        # Plots Buttons
        self.dofPlot.clicked.connect(self.model.plotdof)
        self.frameratePlot.clicked.connect(self.model.plotframerate)
        self.exposurePlot.clicked.connect(self.model.plotmaxexp)

    def on_refractive_change(self):
        try:
            self.model.camera.port_refraction_idx = float(self.refractionLineEdit.text())
        except Exception as e:
            self.refractionLineEdit.setText((str(self.model.camera.port_refraction_idx)))

        self.updateModel()

    def on_camera_info(self):
        if self.model.camera.sensor.initialized:
            print((self.model.camera.sensor.quantum_efficiency_wav))
            print((self.model.camera.sensor.quantum_efficiency))
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
                self.focalLengthLineEdit.setText(("%f" % lens.focal_length))
                self.transmittanceLineEdit.setText(("%f" % lens.transmittance))
                logging.info("Loaded Lens.")
                self.updateModel()

    def on_generic_lens_sliders(self):
        """
        Callback executed when either of the focal length or transmittance sliders for a generic custom lens are
        changed
        :return: None
        """
        f = float(self.focalLengthSlider.value())
        t = float(self.transmittanceSlider.value())/100.
        self.model.camera.lens.init_generic_lens(f, t)
        self.focalLengthLineEdit.setText(("%i" % self.focalLengthSlider.value()))
        self.transmittanceLineEdit.setText(("%i" % self.transmittanceSlider.value()))
        logging.info("Created generic lens with focal length %i and transmittance value of %f.",f,t)
        self.updateModel()

    def on_focal_length_change(self):
        try:
            self.focalLengthSlider.setValue(int(self.focalLengthLineEdit.text()))
            self.on_generic_lens_sliders()
        except Exception as e:
            self.focalLengthLineEdit.setText(("%i" % self.focalLengthSlider.value()))

    def on_transmittance_change(self):
        try:
            self.transmittanceSlider.setValue(int(self.transmittanceLineEdit.text()))
            self.on_generic_lens_sliders()
        except Exception as e:
            self.transmittanceLineEdit.setText(("%i" % self.transmittanceSlider.value()))

    def on_lens_combobox(self, index):
        """
        Callback executed when the lens type combobox is changed.
        :param index: New combobox page index (0=Custom, 1=Generic)
        :return: None
        """
        if index == 1:
            logging.info("Changing to generic lens model")
            self.on_generic_lens_sliders()
        elif index == 0:
            logging.info("Changing to custom lens model")
            self.lensLoadedFileLabel.setText("No File Loaded")
            self.focalLengthLineEdit.setText("0")
            self.model.camera.lens.reset()
        self.updateModel()

    def on_camera_combobox(self, index):
        name = self.cameraComboBox.currentText()
        if name != "Custom":
            filename = self.sensor_dict[name]
            self.load_sensor(filename)

    def on_load_camera(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', QtCore.QDir.homePath())
        self.load_sensor(filename)
        index = self.cameraComboBox.findText("Custom", QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.cameraComboBox.setCurrentIndex(index)

    def load_sensor(self, filename):
        sensor = self.model.camera.sensor
        if os.path.isfile(filename):
            if sensor.load(filename):
                self.pixelSizeValueLabel.setNum(sensor.pixel_size)
                self.resolutionxValueLabel.setNum(sensor.resolution_x)
                self.resolutionyValueLabel.setNum(sensor.resolution_y)
                self.sensorNameLabel.setText(sensor.name)
                self.cameraLoadedFileLabel.setText(os.path.basename(filename))
                self.updateModel()

                logging.info("Loaded Sensor.")

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
        self.beamAngleSlider.setValue(min(self.beamAngleSlider.value(), 89))
        self.model.light.init_generic_led_light(self.luminousFluxLineEdit.text(),
                                                    float(self.beamAngleSlider.value()))
        self.beamAngleLineEdit.setText(("%i" % self.beamAngleSlider.value()))
        self.updateModel()

    def on_beam_angle_change(self):
        try:
            self.beamAngleSlider.setValue(int(self.beamAngleLineEdit.text()))
            self.init_generic_led()
        except Exception as e:
            self.beamAngleLineEdit.setText(("%i" % self.beamAngleSlider.value()))

    def on_dome_radius_change(self):
        try:
            self.model.camera.dome_radius = float(self.domeRadiusLineEdit.text())/100.
        except Exception as e:
            self.domeRadiusLineEdit.setText(("%.1f" % (self.model.camera.dome_radius*100.)))
        self.updateModel()

    def on_dome_thickness_change(self):
        try:
            self.model.camera.dome_thickness = float(self.domeThicknessLineEdit.text())/100.
        except Exception as e:
            self.domeThicknessLineEdit.setText(("%.1f" % (self.model.camera.dome_thickness*100.)))
        self.updateModel()

    def on_altitude_slider(self):
        self.model.scene.altitude = float(self.altitudeSlider.value())/10.
        self.altitudeLineEdit.setText(("%.1f" % self.model.scene.altitude))
        logging.info("Modified altitude to %.1f", self.model.scene.altitude)
        self.updateModel()

    def on_altitude_change(self):
        try:
            self.altitudeSlider.setValue(float(self.altitudeLineEdit.text())*10)
            self.on_altitude_slider()
        except Exception as e:
            self.altitudeLineEdit.setText(("%.1f" % float(self.altitudeSlider.value())/10.))

    def on_overlap_slider(self):
        self.model.scene.overlap = float(self.overlapSlider.value())/100.
        self.overlapLineEdit.setText(("%i" % self.overlapSlider.value()))
        logging.info("Modified overlap to %.2f", self.model.scene.overlap)
        self.updateModel()

    def on_overlap_change(self):
        try:
            self.overlapSlider.setValue(int(self.overlapLineEdit.text()))
            self.on_overlap_slider()
        except Exception as e:
            self.overlapLineEdit.setText(("%i" % self.overlapSlider.value()))

    def on_speed_slider(self):
        self.model.scene.speed = float(self.speedSlider.value())/10.
        self.speedLineEdit.setText(("%.1f" % self.model.scene.speed))
        logging.info("Modified speed to %.1f", self.model.scene.speed)
        self.updateModel()

    def on_speed_change(self):
        try:
            self.speedSlider.setValue(float(self.speedLineEdit.text())*10.)
            self.on_speed_slider()
        except Exception as e:
            self.speedLineEdit.setText(("%.1f" % float(self.speedSlider.value())/10.))

    def on_motionblur_slider(self):
        self.model.scene.motion_blur = float(self.motionBlurSlider.value())
        self.motionBlurLineEdit.setText(("%i" % self.model.scene.motion_blur))
        logging.info("Modified max motion blur to %i", self.model.scene.motion_blur)
        self.updateModel()

    def on_motionblur_change(self):
        try:
            self.motionBlurSlider.setValue(int(self.motionBlurLineEdit.text()))
            self.on_motionBlur_slider()
        except Exception as e:
            self.motionBlurLineEdit.setText(("%i" % self.motionBlurSlider.value()))

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
            self.domeRadiusLabel.hide()
            self.domeRadiusLineEdit.hide()
            self.domeRadiusUnitsLabel.hide()
            self.domeThicknessLabel.hide()
            self.domeThicknessLineEdit.hide()
            self.domeThicknessUnitsLabel.hide()
            self.domeDistanceLabel.hide()
            self.domeDistanceValueLabel.hide()
            self.domeDistanceUnitsLabel.hide()
        elif index == 1:
            self.model.camera.set_housing('domed')
            self.domeRadiusLabel.show()
            self.domeRadiusLineEdit.show()
            self.domeRadiusUnitsLabel.show()
            self.domeThicknessLabel.show()
            self.domeThicknessLineEdit.show()
            self.domeThicknessUnitsLabel.show()
            self.domeDistanceLabel.show()
            self.domeDistanceValueLabel.show()
            self.domeDistanceUnitsLabel.show()
        else:
            logging.error("Invalid housing option in callback")
        self.updateModel()

    def on_bottom_combo(self, index):
        self.model.scene.set_bottom_type(self.bottomTypeCombo.currentText())
        self.updateModel()

    def on_aperture_slider(self):
        self.model.aperture = float(self.chosenApertureSlider.value()) / 10.
        self.apertureLineEdit.setText("%.1f" % self.model.aperture)
        logging.info("Modified aperture to %.1f.", self.model.aperture)
        self.updateModel()

    def on_aperture_change(self):
        try:
            self.chosenApertureSlider.setValue(float(self.apertureLineEdit.text())*10)
            self.on_aperture_slider()
        except Exception as e:
            self.apertureLineEdit.setText("%.1f" % (float(self.chosenApertureSlider.value())/10.))

    def on_gain_slider(self):
        self.model.camera.sensor.user_gain = float(self.gainSlider.value()) / 10.
        self.gainLineEdit.setText("%.1f" % self.model.camera.sensor.user_gain)
        logging.info("Modified gain to %.1f.", self.model.camera.sensor.user_gain)
        self.updateModel()

    def on_gain_change(self):
        try:
            self.gainSlider.setValue(float(self.gainLineEdit.text())*10)
            self.on_gain_slider()
        except Exception as e:
            self.gainLineEdit.setText("%.1f" % (float(self.gainSlider.value())/10.))

    def on_exposure_slider(self):
        exposure = float(self.chosenExposureSlider.value())/1000000.
        if exposure > self.model.max_exposure:
            self.model.exposure = self.model.max_exposure
            self.update_exposure_slider()
        else:
            self.model.exposure = exposure
        self.chosenExposureLineEdit.setText(("%.2f" % (self.model.exposure*1000.)))
        logging.info("Modified exposure to %.2fms", (self.model.exposure*1000.))
        self.updateModel()

    def update_exposure_slider(self):
        self.chosenExposureSlider.setValue(self.model.exposure*1000000.)

    def on_exposure_change(self):
        try:
            self.chosenExposureSlider.setValue(float(self.chosenExposureLineEdit.text())*1000.)
            self.on_exposure_slider()
        except Exception as e:
            self.chosenExposureLineEdit.setText(("%.2f" % (self.model.exposure*1000.)))

    def updateModel(self):
        self.model.update()
        self.updateUI()

    def updateUI(self):
        self.fovxValueLabel.setText(("%.2f" % self.model.fov_x))
        self.fovyValueLabel.setText("%.2f" % self.model.fov_y)
        self.fovxDegValueLabel.setText("%.2f" % (self.model.fov_x_deg*180./pi))
        self.fovyDegValueLabel.setText("%.2f" % (self.model.fov_y_deg*180./pi))
        self.exposureValueLabel.setText("%.2f" % (self.model.max_exposure*1000.))
        self.framerateValueLabel.setText("%.2f" % self.model.framerate)
        self.effectiveFocalLengthValueLabel.setText("%.2f" % self.model.eff_focal_length)
        self.avgImgValueValueLabel.setText("%.2f" % self.model.response)
        self.dofNearValueLabel.setText("%.1f" % (self.model.scene.depthoffield[0]))
        self.dofFarValueLabel.setText("%.1f" % (self.model.scene.depthoffield[1]))
        self.chosenExposureSlider.setMaximum(int(self.model.max_exposure*1000000))
        if float(self.chosenExposureLineEdit.text())/1000. > self.model.max_exposure:
            self.chosenExposureLineEdit.setText("%.2f" % (self.model.max_exposure*1000.))
            self.update_exposure_slider()
        self.snrValueLabel.setText(("%.2f" % self.model.snr))
        self.domeDistanceValueLabel.setText(("%.2f" % self.model.dome_virtual_distance))

class Model:
    def __init__(self):
        self.camera = Camera()
        self.light = LightSource()
        self.scene = OperationalParameters()
        self.water = WaterPropagation()

        self.fov_x = 0.
        self.fov_y = 0.
        self.fov_x_deg = 0.
        self.fov_y_deg = 0.
        self.aperture = 2.
        self.exposure = 0.
        self.max_exposure = 1.
        self.framerate = 0.
        self.eff_focal_length = 0.
        self.response = 0.
        self.snr = 0.
        self.dome_virtual_distance = 0.

    def update(self):
        logging.info("Updating model")
        if self.camera.lens.initialized:
            self.eff_focal_length = self.camera.effective_focal_length
        else:
            self.eff_focal_length = 0.

        if self.camera.initialized():
            self.fov_x = self.camera.get_fov('x', self.scene.altitude)
            self.fov_y = self.camera.get_fov('y', self.scene.altitude)
            self.fov_x_deg = self.camera.get_angular_fov('x')
            self.fov_y_deg = self.camera.get_angular_fov('y')
            self.max_exposure = self.camera.max_blur_shutter_time(self.scene.axis, self.scene.altitude,
                                                              self.scene.speed, self.scene.motion_blur)
            self.framerate = self.camera.compute_framerate(self.scene.axis, self.scene.altitude,
                                                           self.scene.speed, self.scene.overlap)
            self.scene.depthoffield = self.camera.get_depth_of_field(self.aperture, self.scene.altitude)
            self.dome_virtual_distance = 100.*self.camera.dome_world_to_virtual_dist((self.scene.altitude))

        else:
            self.fov_y = 0.
            self.fov_x = 0.
            self.framerate = 0.


        if self.camera.initialized() and self.water.initialized and self.light.initialized:
            logging.info("Updating full image formation model")

            lights_wavelength, lights_irradiance_spectrum = self.light.get_irradiance_spectrum(self.scene.altitude)
            print((np.max(lights_irradiance_spectrum)))
            water_attenuation = [self.water.get_attenuation(x, self.scene.altitude) for x in lights_wavelength]
            print((np.max(water_attenuation)))
            # TODO: Get reflection value
            # reflection = [0.53] * len(lights_wavelength)
            reflection = [self.scene.get_reflectance()] * len(lights_wavelength)
            print(("Reflectance: {}".format(self.scene.get_reflectance())))

            lens_transmittance = [self.camera.lens.get_transmittance(x)*
                                  self.camera.lens.lens_aperture_attenuation(self.aperture)
                                  for x in lights_wavelength]
            incident_spectrum = lights_irradiance_spectrum * np.power(water_attenuation, 2) * reflection * lens_transmittance

            # TODO: Currently assumes all sensor parameters given relative to 16bit pixel response
            self.response = (self.camera.sensor.compute_digital_signal_broadband(self.exposure,
                                                                                lights_wavelength,
                                                                                incident_spectrum)/2**16)*100
            self.snr = self.camera.sensor.compute_signal_to_noise_ratio(self.exposure, lights_wavelength, incident_spectrum)


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
        exposure = self.camera.vectorized_exposure(self.scene.axis, dd, ss, self.scene.motion_blur)*1000.

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_title("Max exposure")
        ax.set_xlabel("Speed [m/s]")
        ax.set_ylabel("Target Distance [m]")
        ax.set_zlabel("Max exposure [ms]")
        surf = ax.plot_surface(ss, dd, exposure)
        plt.show()

    def plotdof(self):
        N = np.arange(1, 6, 0.1)
        d = np.arange(0.5, 2.0, .01)
        nn, dd = np.meshgrid(N, d)
        res = self.camera.vectorized_dof(nn, dd)


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
    # app.setWindowIcon(QtGui.QIcon('/home/eiscar/PyCharm_Projects/UWOpticalSystemDesigner/resources/light_model.png'))
    form = UnderwaterOpticalCalculatorApp()  # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()
    logging.info('Finished')

if __name__=="__main__":
    main()
