from PyQt5 import QtCore, QtGui, QtWidgets
from camera import Camera, LightSource, OperationalParameters

import mainwindow
import sys
import os
import logging

class UnderwaterOpticalCalculatorApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined

        self.connections()

        self.model = Model()

    def connections(self):
        """
        Sets up the required connections of the
        :return:
        """

        # Lens connections
        self.lensLoadFileButton.clicked.connect(self.on_load_lens)
        self.LensComboBox.currentIndexChanged.connect(self.on_lens_combobox)
        self.focalLengthSlider.valueChanged.connect(self.on_generic_lens_sliders)
        self.transmittanceSlider.valueChanged.connect(self.on_generic_lens_sliders)

        # Camera connections
        self.cameraLoadFileButton.clicked.connect(self.on_load_camera)

        # Scene connections
        self.altitudeSlider.valueChanged.connect(self.on_altitude_slider)
        self.overlapSlider.valueChanged.connect(self.on_overlap_slider)
        self.speedSlider.valueChanged.connect(self.on_speed_slider)
        self.motionBlurSlider.valueChanged.connect(self.on_motionblur_slider)
        self.dofSlider.valueChanged.connect(self.on_depthoffield_slider)

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

    def on_load_camera(self):

        sensor = self.model.camera.sensor

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', QtCore.QDir.homePath())

        if os.path.isfile(filename):
            if sensor.load(filename):
                self.pixelSizeValueLabel.setNum(sensor.pixel_size)
                self.resolutionxValueLabel.setNum(sensor.resolution_x)
                self.resolutionyValueLabel.setNum(sensor.resolution_y)
                self.sensorNameLabel.setText(sensor.name)
                logging.info("Loaded Lens.")

    def on_light_combobox(self, index):
        if index == 0:
            # Generic LED light
            self.model.light.init_generic_led_light()
        elif index == 1:
            pass
        elif index == 2:
            pass
        elif index == 3:
            pass






    def on_altitude_slider(self):
        self.model.scene.altitude = self.altitudeSlider.value()/100
        logging.info("Modified altitude to %f.", self.model.scene.altitude)

    def on_overlap_slider(self):
        self.model.scene.overlap = self.overlapSlider.value()
        logging.info("Modified overlap to %i.", self.model.scene.overlap)

    def on_speed_slider(self):
        self.model.scene.speed = self.speedSlider.value()/100
        logging.info("Modified speed to %f.", self.model.scene.speed)

    def on_motionblur_slider(self):
        self.model.scene.motion_blur = self.motionBlurSlider.value()
        logging.info("Modified max motion blur to %i.", self.model.scene.motion_blur)

    def on_depthoffield_slider(self):
        self.model.scene.depthoffield = self.dofSlider.value()/100
        logging.info("Modified overlap to %f.", self.model.scene.depthoffield)

    def test(self):
        print("Test!")

class Model():
    def __init__(self):
        self.camera = Camera()
        self.light = LightSource()
        self.scene = OperationalParameters()



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