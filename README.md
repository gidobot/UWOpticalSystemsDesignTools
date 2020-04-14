# Underwater Optical System Design Tool
This tool acts as a simple "back of the envelope" calculator to guide camera and lighting choices, when designing an underwater camera system. The tool is designed with imaging survey platforms in mind, such as a diver operated rig or an AUV with downward facing camera and strobes.

The tool encorporates modelng of the source lighting spectrum, physical modeling of spectrum dependent light propogation through different water bodies, lensing effects, and manufacturer specified camera sensor response functions to provide realistic estimates of imaging performance, based on a set of input operational parameters.

## Python Dependencies: 
Pyqt5
SIP

## Tool Use

From src folder, launch GUI as  
`python main.py`

Example image of the user interface  
![alt text](resources/interface.png)

The interface is divided into three sections, where the top section is hardware and lighting configuration, the middle section is input operational parameters, and the bottom section is the output performance and constraints of the imaging system. Following are brief descriptions of the different paramters.  

#### Lights

#### Underwater Attenuation

#### Lens

#### Camera

#### Altitude

#### Overlap

#### Speed

#### Max Motion Blur

#### Aperture

#### Camera Orientation

#### Housing Viewport Type

#### Bottom Type

#### Near and Far Depth of Field Limits

#### Max Exposure and Exposure Time

#### FOV x and FOV y

#### Avg Image Intensity

#### Min Framerate

## Generate UI

To generate the UI use Qt Creator. 
Changes to the UI file have to be converted to python with: 
```pyuic5 qt/UWOpticalSystemDesigner/mainwindow.ui -o src/mainwindow.py```
