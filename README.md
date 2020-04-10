# Underwater Optical System Design Tool
This tool acts as a simple "back of the envelope" calculator to guide camera and lighting choices, when designing an underwater camera system. The tool is designed with imaging survey platforms in mind, such as a diver operated rig or an AUV with downward facing camera and strobes.

The tool encorporates modelng of the source lighting spectrum, physical modeling of spectrum dependent light propogation through different water bodies, lensing effects, and manufacturer specified camera sensor response functions to provide realistic estimates of imaging performance, based on a set of input operational parameters.

# Tool Use

From src folder, launch tool GUI as  
`python main.py`

## Python Dependencies: 
Pyqt5
SIP

## Generate UI

To generate the UI use Qt Creator. 
Changes to the UI file have to be converted to python with: 
```pyuic5 qt/UWOpticalSystemDesigner/mainwindow.ui -o src/mainwindow.py```
