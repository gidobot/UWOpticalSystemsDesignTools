# Underwater Optical System Design Tool
This tool acts as a simple "back of the envelope" calculator to guide camera and lighting design choices in an underwater camera system. The tool is designed with imaging survey platforms in mind, such as a diver operated rig or an AUV with downward facing camera and strobes.

The tool encorporates modelng of the source lighting spectrum, physical modeling of spectrum dependent light propogation through different water bodies, lensing effects, and manufacturer specified camera sensor response functions to provide realistic estimates of imaging performance, based on a set of input operational parameters.

## Python Dependencies: 
Pyqt5
SIP

## Tool Use

From src folder, launch GUI as  
`python main.py`

Example image of the user interface  
![alt text](resources/interface.png)

The interface is divided into three sections: where the top section is hardware and lighting configuration, the middle section is input operational parameters, and the bottom section is the output performance and constraints of the imaging system. Following are brief descriptions of the different paramters.  

#### Lights

Currently the software only supports a generic LED spectrum as the light source, though other sources are included as menu options.

#### Underwater Attenuation

This option sets the type of water in which the imaging system is expected to operate, based on the Jerlov classification scale. The poorest expected water type should be selected here for system design. More information about the Jerlov classification scheme can be found here  
http://www.oceanopticsbook.info/view/overview_of_optical_oceanography/classification_schemes

#### Lens

Though custom lens specification files may be provided, the generic lens profile is generally good enough for most optics used in the field. Lens transmittance efficency is generally 80-90%.

#### Camera

A dropdown menu of common machine vision sensors are provided. The tool makes it easy to compare different imaging sensors. The selection menu is auto-populated by the configuration files found in the cfg/sensors folder. New sensor configuration files may be added to this folder and will appear in the menu. Also, configuration files can be loaded from custom locations in the interface.

#### Altitude

Target height-from-bottom at which imaging system will operate, or the expected working distance to imaging subject.

#### Overlap

In the context of an imaging survey of the seabed, this is the desired percentage overlap between consecutive images.

#### Speed

Speed of imaging system motion along survey path.

#### Max Motion Blur

Maximum allowable pixel blur in the aquired images. For feature matching applications, this is generally desired to be 1 pixel.

#### Aperture

Camera aperture should be set based on the desired depth of field limits displayed in the output section.

#### Camera Orientation

The orientation of the camera referenced to the primary axis of motion. Portrait orientation sets the image width along the axis of motion.

#### Housing Viewport Type

Viewport can be set to flat or dome, though the dome type is not yet fully supported in the software.

#### Bottom Type

The type of bottom expected to be imaged is an important consideration. Sand bottom reflects the most light, while organic bottoms reflect the least and require more light or exposure time to image. The bottom type is represented by a single value benthic reflection coefficient coarsly estimated from here  
http://www.ioccg.org/training/SLS-2016/Dierssen_IOCCG_Lecture1_webLO.pdf

Spectrum dependence is not considered in the reflection coefficient, as this varies greatly across specific imaging subjects. Support is planned to be added in the future for custom spectrum dependent reflectance profiles.

#### Near and Far Depth of Field Limits

The depth of field limits represent the imaging range at which the subject remains in acceptable focus. These values should be tuned by the aperture setting based on operational requirements. It is desirable to keep the aperture value as low as possible to reduce lighting requirements, so this paramter should be tuned carefully.

#### Max Exposure and Exposure Time

The maximum exposure time is calculated based on the maximum pixel blur and the speed of motion. The actual exposure time of the system can be set to the max exposure time or lower.

#### FOV x and FOV y

The angular field of view in the x and y imaging axes are reported as well as the spacial field of view based on the imaging altitude.

#### Avg Image Intensity

The average image intensity is the primary output that dictates hardware and lighting requirements. This value is calculated based on all optical, operational, and envrionmental parameters. The tool assumes no gain is added to the sensor response, but this may be added as an additional parameter in the future with a signal to noise reponse estimate. As a rule of thumb, a good target average image intensity for underwater is ~30%.

#### Min Framerate

The minimum framerate is calcualted based on the speed of the imaging system and the desired minimum overlap between consecutive image frames.

## Generate UI

To generate the UI use Qt Creator. 
Changes to the UI file have to be converted to python with: 
```pyuic5 qt/UWOpticalSystemDesigner/mainwindow.ui -o src/mainwindow.py```
