from PyQt5 import QtCore, QtGui, QtWidgets
from camera import Camera,  OperationalParameters
from lights import LightSource
from wateratenuationmodel import WaterPropagation
from plotWindows import GraphWindow

import mainwindow
import sys
import os
import logging

class UnderwaterOpticalCalculatorApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically

        self.connections()

        self.model = Model()
        self.init_model()

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
            pass
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

    def on_altitude_slider(self):
        self.model.scene.altitude = self.altitudeSlider.value()/100
        logging.info("Modified altitude to %f.", self.model.scene.altitude)
        self.updateModel()

    def on_overlap_slider(self):
        self.model.scene.overlap = self.overlapSlider.value()/100
        logging.info("Modified overlap to %i.", self.model.scene.overlap)
        self.updateModel()

    def on_speed_slider(self):
        self.model.scene.speed = self.speedSlider.value()/100
        logging.info("Modified speed to %f.", self.model.scene.speed)
        self.updateModel()

    def on_motionblur_slider(self):
        self.model.scene.motion_blur = self.motionBlurSlider.value()
        logging.info("Modified max motion blur to %i.", self.model.scene.motion_blur)
        self.updateModel()

    def on_depthoffield_slider(self):
        self.model.scene.depthoffield = self.dofSlider.value()/100
        logging.info("Modified overlap to %f.", self.model.scene.depthoffield)
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

    def updateModel(self):
        self.model.update()
        self.updateUI()

    def updateUI(self):
        self.fovxValueLabel.setText(("%.2f" % self.model.fov_x))
        self.fovyValueLabel.setText("%.2f" % self.model.fov_y)
        self.exposureValueLabel.setText("%.2f" % (self.model.exposure*1000))
        self.framerateValueLabel.setText("%.2f" % self.model.framerate)
        self.apertureValueLabel.setText("%.2f" % self.model.aperture)
        self.effectiveFocalLengthValueLabel.setText("%.2f" % self.model.eff_focal_length)

    def test(self):
        print("Test!")

class Model:
    def __init__(self):
        self.camera = Camera()
        self.light = LightSource()
        self.scene = OperationalParameters()
        self.water = WaterPropagation()

        self.fov_x = 0
        self.fov_y = 0
        self.aperture = 0
        self.exposure = 0
        self.framerate = 0
        self.eff_focal_length = 0

    def update(self):
        logging.info("Updating model")
        if self.camera.lens.initialized:
            self.eff_focal_length = self.camera.effective_focal_length
        else:
            self.eff_focal_length = 0

        if self.camera.initialized():
            self.fov_x = self.camera.get_fov('x', self.scene.altitude)
            self.fov_y = self.camera.get_fov('y', self.scene.altitude)
            self.exposure = self.camera.max_blur_shutter_time(self.scene.axis, self.scene.altitude,
                                                              self.scene.speed, self.scene.motion_blur)
            self.framerate = self.camera.compute_framerate(self.scene.axis, self.scene.altitude,
                                                           self.scene.speed, self.scene.overlap)
            self.aperture = self.camera.compute_aperture(self.scene.depthoffield, self.scene.altitude)

        else:
            self.fov_y = 0
            self.fov_x = 0
            self.exposure = 0
            self.framerate = 0
            self.aperture = 0

        if self.camera.initialized() and self.water.initialized and self.light.initialized:
            logging.info("Updating full image formation model")

            lights_wavelength, lights_irradiance_spectrum = self.light.get_irradiance_spectrum(self.scene.altitude)
            print(max(lights_wavelength))
            print(min(lights_wavelength))
            water_attenuation = [self.water.get_attenuation(x, self.scene.altitude) for x in lights_wavelength]
            # TODO: Get reflection value
            reflection = [0.53] * len(water_attenuation)

            lens_transmittance = [self.camera.lens.get_transmittance(x) for x in lights_wavelength]
            #incident_spectrum = lights_irradiance_spectrum * water_attenuation**2 * reflection * lens_transmittance

            # Compute irradiance


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