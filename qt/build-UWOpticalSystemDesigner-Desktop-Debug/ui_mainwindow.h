/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.2.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QStackedWidget>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout;
    QGroupBox *LightBox;
    QVBoxLayout *verticalLayout_2;
    QHBoxLayout *horizontalLayout_2;
    QLabel *label;
    QComboBox *LightsComboBox;
    QStackedWidget *lightStackedWidget;
    QWidget *page_2;
    QVBoxLayout *verticalLayout_7;
    QPushButton *lightsLoadFileButton;
    QLabel *lightsLoadedFileLabel;
    QSpacerItem *verticalSpacer;
    QWidget *page;
    QGridLayout *gridLayout;
    QSpacerItem *verticalSpacer_5;
    QLabel *label_21;
    QLabel *label_3;
    QWidget *page_3;
    QGridLayout *gridLayout_7;
    QLabel *label_27;
    QSpacerItem *verticalSpacer_6;
    QWidget *page_4;
    QGridLayout *gridLayout_6;
    QLabel *label_20;
    QSpacerItem *verticalSpacer_7;
    QWidget *page_5;
    QGridLayout *gridLayout_8;
    QLabel *label_28;
    QSpacerItem *verticalSpacer_8;
    QGridLayout *gridLayout_5;
    QLabel *luminousFluxLabel;
    QSlider *beamAngleSlider;
    QLabel *beamAngleLabel;
    QLabel *beamAngleValueLabel;
    QLineEdit *luminousFluxLineEdit;
    QLabel *beamAngleUnitsLabel;
    QLabel *liminousFluxUnitsLabel;
    QSpacerItem *horizontalSpacer_6;
    QFrame *verticalLineLeft;
    QGroupBox *LensBox;
    QVBoxLayout *verticalLayout_5;
    QGridLayout *gridLayout_2;
    QComboBox *LensComboBox;
    QLabel *label_2;
    QStackedWidget *lensStackedWidget;
    QWidget *page_9;
    QVBoxLayout *verticalLayout_8;
    QPushButton *lensLoadFileButton;
    QLabel *lensLoadedFileLabel;
    QHBoxLayout *horizontalLayout_6;
    QLabel *focalLengthLabel;
    QLabel *focalLengthValueLabel;
    QLabel *focalLengthUnitsLabel;
    QWidget *page_10;
    QGridLayout *gridLayout_10;
    QLabel *label_32;
    QLabel *label_34;
    QSlider *transmittanceSlider;
    QLabel *focalLenthSliderUnitsLabel;
    QLabel *transmittanceValueLabel;
    QLabel *transmittanceUnitsLabel;
    QLabel *focalLengthSliderValueLabel;
    QSlider *focalLengthSlider;
    QSpacerItem *verticalSpacer_4;
    QFrame *line_3;
    QGroupBox *SensorBox;
    QVBoxLayout *verticalLayout_6;
    QVBoxLayout *verticalLayout_3;
    QHBoxLayout *horizontalLayout_5;
    QLabel *cameraTypeLabel;
    QComboBox *cameraComboBox;
    QStackedWidget *cameraStackedWidget;
    QWidget *page_12;
    QGridLayout *gridLayout_11;
    QPushButton *cameraLoadFileButton;
    QLabel *cameraLoadedFileLabel;
    QGridLayout *gridLayout_9;
    QLabel *resolutionyLabel;
    QLabel *resolutionxLabel;
    QLabel *pixelSizeLabel;
    QLabel *pixelSizeUnitsLabel;
    QLabel *pixelSizeValueLabel;
    QLabel *resolutionxValueLabel;
    QLabel *resolutionxUnitsLabel;
    QLabel *resolutionyValueLabel;
    QLabel *resolutionyUnitsLabel;
    QLabel *label_11;
    QLabel *sensorNameLabel;
    QWidget *page_13;
    QSpacerItem *horizontalSpacer_3;
    QFrame *line_2;
    QGroupBox *SceneBox;
    QGridLayout *gridLayout_3;
    QLabel *overlapValueLabel;
    QLabel *label_8;
    QLabel *altitudeLabel;
    QLabel *label_7;
    QLabel *label_6;
    QLabel *label_5;
    QLabel *label_4;
    QSlider *overlapSlider;
    QLabel *label_15;
    QLabel *speedValueLabel;
    QLabel *speedUnitsLabel;
    QSlider *speedSlider;
    QSpacerItem *horizontalSpacer_2;
    QLabel *altitudeUnitsLabel;
    QComboBox *bottomTypeCombo;
    QSlider *altitudeSlider;
    QLabel *label_17;
    QLabel *dofUnitsLabel;
    QLabel *dofValueLabel;
    QLabel *motionBlurUnitsLabel;
    QLabel *motionBlurValueLabel;
    QSlider *motionBlurSlider;
    QSlider *dofSlider;
    QFrame *line_4;
    QGroupBox *OutputBox;
    QGridLayout *gridLayout_4;
    QSpacerItem *verticalSpacer_2;
    QLabel *FOVyLabel;
    QLabel *FOVxLabel;
    QLabel *apertureLabel;
    QLabel *exposureLabel;
    QFrame *line_5;
    QHBoxLayout *horizontalLayout_7;
    QPushButton *saveButton;
    QPushButton *loadButton;
    QPushButton *exportButton;
    QMenuBar *menuBar;
    QMenu *menuUnderwater_Optical_Systems_Calculator;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(1202, 677);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        verticalLayout = new QVBoxLayout(centralWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        LightBox = new QGroupBox(centralWidget);
        LightBox->setObjectName(QStringLiteral("LightBox"));
        LightBox->setEnabled(true);
        LightBox->setFlat(false);
        LightBox->setCheckable(false);
        verticalLayout_2 = new QVBoxLayout(LightBox);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setContentsMargins(11, 11, 11, 11);
        verticalLayout_2->setObjectName(QStringLiteral("verticalLayout_2"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        label = new QLabel(LightBox);
        label->setObjectName(QStringLiteral("label"));

        horizontalLayout_2->addWidget(label);

        LightsComboBox = new QComboBox(LightBox);
        LightsComboBox->setObjectName(QStringLiteral("LightsComboBox"));

        horizontalLayout_2->addWidget(LightsComboBox);


        verticalLayout_2->addLayout(horizontalLayout_2);

        lightStackedWidget = new QStackedWidget(LightBox);
        lightStackedWidget->setObjectName(QStringLiteral("lightStackedWidget"));
        page_2 = new QWidget();
        page_2->setObjectName(QStringLiteral("page_2"));
        verticalLayout_7 = new QVBoxLayout(page_2);
        verticalLayout_7->setSpacing(6);
        verticalLayout_7->setContentsMargins(11, 11, 11, 11);
        verticalLayout_7->setObjectName(QStringLiteral("verticalLayout_7"));
        lightsLoadFileButton = new QPushButton(page_2);
        lightsLoadFileButton->setObjectName(QStringLiteral("lightsLoadFileButton"));

        verticalLayout_7->addWidget(lightsLoadFileButton);

        lightsLoadedFileLabel = new QLabel(page_2);
        lightsLoadedFileLabel->setObjectName(QStringLiteral("lightsLoadedFileLabel"));

        verticalLayout_7->addWidget(lightsLoadedFileLabel);

        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_7->addItem(verticalSpacer);

        lightStackedWidget->addWidget(page_2);
        page = new QWidget();
        page->setObjectName(QStringLiteral("page"));
        gridLayout = new QGridLayout(page);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        verticalSpacer_5 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout->addItem(verticalSpacer_5, 2, 0, 1, 1);

        label_21 = new QLabel(page);
        label_21->setObjectName(QStringLiteral("label_21"));

        gridLayout->addWidget(label_21, 0, 0, 1, 1);

        label_3 = new QLabel(page);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setWordWrap(true);

        gridLayout->addWidget(label_3, 1, 0, 1, 1);

        lightStackedWidget->addWidget(page);
        page_3 = new QWidget();
        page_3->setObjectName(QStringLiteral("page_3"));
        gridLayout_7 = new QGridLayout(page_3);
        gridLayout_7->setSpacing(6);
        gridLayout_7->setContentsMargins(11, 11, 11, 11);
        gridLayout_7->setObjectName(QStringLiteral("gridLayout_7"));
        label_27 = new QLabel(page_3);
        label_27->setObjectName(QStringLiteral("label_27"));

        gridLayout_7->addWidget(label_27, 0, 0, 1, 1);

        verticalSpacer_6 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_7->addItem(verticalSpacer_6, 1, 0, 1, 1);

        lightStackedWidget->addWidget(page_3);
        page_4 = new QWidget();
        page_4->setObjectName(QStringLiteral("page_4"));
        gridLayout_6 = new QGridLayout(page_4);
        gridLayout_6->setSpacing(6);
        gridLayout_6->setContentsMargins(11, 11, 11, 11);
        gridLayout_6->setObjectName(QStringLiteral("gridLayout_6"));
        label_20 = new QLabel(page_4);
        label_20->setObjectName(QStringLiteral("label_20"));

        gridLayout_6->addWidget(label_20, 0, 0, 1, 1);

        verticalSpacer_7 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_6->addItem(verticalSpacer_7, 1, 0, 1, 1);

        lightStackedWidget->addWidget(page_4);
        page_5 = new QWidget();
        page_5->setObjectName(QStringLiteral("page_5"));
        gridLayout_8 = new QGridLayout(page_5);
        gridLayout_8->setSpacing(6);
        gridLayout_8->setContentsMargins(11, 11, 11, 11);
        gridLayout_8->setObjectName(QStringLiteral("gridLayout_8"));
        label_28 = new QLabel(page_5);
        label_28->setObjectName(QStringLiteral("label_28"));

        gridLayout_8->addWidget(label_28, 0, 0, 1, 1);

        verticalSpacer_8 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_8->addItem(verticalSpacer_8, 1, 0, 1, 1);

        lightStackedWidget->addWidget(page_5);

        verticalLayout_2->addWidget(lightStackedWidget);

        gridLayout_5 = new QGridLayout();
        gridLayout_5->setSpacing(6);
        gridLayout_5->setObjectName(QStringLiteral("gridLayout_5"));
        gridLayout_5->setContentsMargins(-1, 0, -1, -1);
        luminousFluxLabel = new QLabel(LightBox);
        luminousFluxLabel->setObjectName(QStringLiteral("luminousFluxLabel"));

        gridLayout_5->addWidget(luminousFluxLabel, 0, 0, 1, 1);

        beamAngleSlider = new QSlider(LightBox);
        beamAngleSlider->setObjectName(QStringLiteral("beamAngleSlider"));
        beamAngleSlider->setMinimum(1);
        beamAngleSlider->setMaximum(90);
        beamAngleSlider->setValue(15);
        beamAngleSlider->setOrientation(Qt::Horizontal);

        gridLayout_5->addWidget(beamAngleSlider, 1, 1, 1, 1);

        beamAngleLabel = new QLabel(LightBox);
        beamAngleLabel->setObjectName(QStringLiteral("beamAngleLabel"));

        gridLayout_5->addWidget(beamAngleLabel, 1, 0, 1, 1);

        beamAngleValueLabel = new QLabel(LightBox);
        beamAngleValueLabel->setObjectName(QStringLiteral("beamAngleValueLabel"));
        beamAngleValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_5->addWidget(beamAngleValueLabel, 1, 2, 1, 1);

        luminousFluxLineEdit = new QLineEdit(LightBox);
        luminousFluxLineEdit->setObjectName(QStringLiteral("luminousFluxLineEdit"));
        luminousFluxLineEdit->setInputMethodHints(Qt::ImhDigitsOnly);
        luminousFluxLineEdit->setMaxLength(10);
        luminousFluxLineEdit->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_5->addWidget(luminousFluxLineEdit, 0, 1, 1, 1);

        beamAngleUnitsLabel = new QLabel(LightBox);
        beamAngleUnitsLabel->setObjectName(QStringLiteral("beamAngleUnitsLabel"));

        gridLayout_5->addWidget(beamAngleUnitsLabel, 1, 3, 1, 1);

        liminousFluxUnitsLabel = new QLabel(LightBox);
        liminousFluxUnitsLabel->setObjectName(QStringLiteral("liminousFluxUnitsLabel"));

        gridLayout_5->addWidget(liminousFluxUnitsLabel, 0, 2, 1, 1);

        horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_5->addItem(horizontalSpacer_6, 0, 3, 1, 1);


        verticalLayout_2->addLayout(gridLayout_5);


        horizontalLayout->addWidget(LightBox);

        verticalLineLeft = new QFrame(centralWidget);
        verticalLineLeft->setObjectName(QStringLiteral("verticalLineLeft"));
        verticalLineLeft->setFrameShape(QFrame::VLine);
        verticalLineLeft->setFrameShadow(QFrame::Sunken);

        horizontalLayout->addWidget(verticalLineLeft);

        LensBox = new QGroupBox(centralWidget);
        LensBox->setObjectName(QStringLiteral("LensBox"));
        verticalLayout_5 = new QVBoxLayout(LensBox);
        verticalLayout_5->setSpacing(6);
        verticalLayout_5->setContentsMargins(11, 11, 11, 11);
        verticalLayout_5->setObjectName(QStringLiteral("verticalLayout_5"));
        gridLayout_2 = new QGridLayout();
        gridLayout_2->setSpacing(6);
        gridLayout_2->setObjectName(QStringLiteral("gridLayout_2"));
        LensComboBox = new QComboBox(LensBox);
        LensComboBox->setObjectName(QStringLiteral("LensComboBox"));

        gridLayout_2->addWidget(LensComboBox, 0, 1, 1, 1);

        label_2 = new QLabel(LensBox);
        label_2->setObjectName(QStringLiteral("label_2"));

        gridLayout_2->addWidget(label_2, 0, 0, 1, 1);


        verticalLayout_5->addLayout(gridLayout_2);

        lensStackedWidget = new QStackedWidget(LensBox);
        lensStackedWidget->setObjectName(QStringLiteral("lensStackedWidget"));
        page_9 = new QWidget();
        page_9->setObjectName(QStringLiteral("page_9"));
        verticalLayout_8 = new QVBoxLayout(page_9);
        verticalLayout_8->setSpacing(6);
        verticalLayout_8->setContentsMargins(11, 11, 11, 11);
        verticalLayout_8->setObjectName(QStringLiteral("verticalLayout_8"));
        lensLoadFileButton = new QPushButton(page_9);
        lensLoadFileButton->setObjectName(QStringLiteral("lensLoadFileButton"));

        verticalLayout_8->addWidget(lensLoadFileButton);

        lensLoadedFileLabel = new QLabel(page_9);
        lensLoadedFileLabel->setObjectName(QStringLiteral("lensLoadedFileLabel"));

        verticalLayout_8->addWidget(lensLoadedFileLabel);

        horizontalLayout_6 = new QHBoxLayout();
        horizontalLayout_6->setSpacing(6);
        horizontalLayout_6->setObjectName(QStringLiteral("horizontalLayout_6"));
        focalLengthLabel = new QLabel(page_9);
        focalLengthLabel->setObjectName(QStringLiteral("focalLengthLabel"));

        horizontalLayout_6->addWidget(focalLengthLabel);

        focalLengthValueLabel = new QLabel(page_9);
        focalLengthValueLabel->setObjectName(QStringLiteral("focalLengthValueLabel"));
        focalLengthValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        horizontalLayout_6->addWidget(focalLengthValueLabel);

        focalLengthUnitsLabel = new QLabel(page_9);
        focalLengthUnitsLabel->setObjectName(QStringLiteral("focalLengthUnitsLabel"));

        horizontalLayout_6->addWidget(focalLengthUnitsLabel);


        verticalLayout_8->addLayout(horizontalLayout_6);

        lensStackedWidget->addWidget(page_9);
        page_10 = new QWidget();
        page_10->setObjectName(QStringLiteral("page_10"));
        gridLayout_10 = new QGridLayout(page_10);
        gridLayout_10->setSpacing(6);
        gridLayout_10->setContentsMargins(11, 11, 11, 11);
        gridLayout_10->setObjectName(QStringLiteral("gridLayout_10"));
        label_32 = new QLabel(page_10);
        label_32->setObjectName(QStringLiteral("label_32"));

        gridLayout_10->addWidget(label_32, 0, 0, 1, 1);

        label_34 = new QLabel(page_10);
        label_34->setObjectName(QStringLiteral("label_34"));

        gridLayout_10->addWidget(label_34, 2, 0, 1, 1);

        transmittanceSlider = new QSlider(page_10);
        transmittanceSlider->setObjectName(QStringLiteral("transmittanceSlider"));
        transmittanceSlider->setMaximum(100);
        transmittanceSlider->setSliderPosition(90);
        transmittanceSlider->setTracking(true);
        transmittanceSlider->setOrientation(Qt::Horizontal);

        gridLayout_10->addWidget(transmittanceSlider, 2, 1, 1, 1);

        focalLenthSliderUnitsLabel = new QLabel(page_10);
        focalLenthSliderUnitsLabel->setObjectName(QStringLiteral("focalLenthSliderUnitsLabel"));

        gridLayout_10->addWidget(focalLenthSliderUnitsLabel, 0, 3, 1, 1);

        transmittanceValueLabel = new QLabel(page_10);
        transmittanceValueLabel->setObjectName(QStringLiteral("transmittanceValueLabel"));
        transmittanceValueLabel->setMinimumSize(QSize(30, 0));
        transmittanceValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_10->addWidget(transmittanceValueLabel, 2, 2, 1, 1);

        transmittanceUnitsLabel = new QLabel(page_10);
        transmittanceUnitsLabel->setObjectName(QStringLiteral("transmittanceUnitsLabel"));

        gridLayout_10->addWidget(transmittanceUnitsLabel, 2, 3, 1, 1);

        focalLengthSliderValueLabel = new QLabel(page_10);
        focalLengthSliderValueLabel->setObjectName(QStringLiteral("focalLengthSliderValueLabel"));
        focalLengthSliderValueLabel->setMinimumSize(QSize(25, 0));
        focalLengthSliderValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_10->addWidget(focalLengthSliderValueLabel, 0, 2, 1, 1);

        focalLengthSlider = new QSlider(page_10);
        focalLengthSlider->setObjectName(QStringLiteral("focalLengthSlider"));
        focalLengthSlider->setMaximum(200);
        focalLengthSlider->setValue(8);
        focalLengthSlider->setTracking(true);
        focalLengthSlider->setOrientation(Qt::Horizontal);

        gridLayout_10->addWidget(focalLengthSlider, 0, 1, 1, 1);

        lensStackedWidget->addWidget(page_10);

        verticalLayout_5->addWidget(lensStackedWidget);

        verticalSpacer_4 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_5->addItem(verticalSpacer_4);


        horizontalLayout->addWidget(LensBox);

        line_3 = new QFrame(centralWidget);
        line_3->setObjectName(QStringLiteral("line_3"));
        line_3->setFrameShape(QFrame::VLine);
        line_3->setFrameShadow(QFrame::Sunken);

        horizontalLayout->addWidget(line_3);

        SensorBox = new QGroupBox(centralWidget);
        SensorBox->setObjectName(QStringLiteral("SensorBox"));
        verticalLayout_6 = new QVBoxLayout(SensorBox);
        verticalLayout_6->setSpacing(6);
        verticalLayout_6->setContentsMargins(11, 11, 11, 11);
        verticalLayout_6->setObjectName(QStringLiteral("verticalLayout_6"));
        verticalLayout_3 = new QVBoxLayout();
        verticalLayout_3->setSpacing(6);
        verticalLayout_3->setObjectName(QStringLiteral("verticalLayout_3"));
        horizontalLayout_5 = new QHBoxLayout();
        horizontalLayout_5->setSpacing(6);
        horizontalLayout_5->setObjectName(QStringLiteral("horizontalLayout_5"));
        cameraTypeLabel = new QLabel(SensorBox);
        cameraTypeLabel->setObjectName(QStringLiteral("cameraTypeLabel"));

        horizontalLayout_5->addWidget(cameraTypeLabel);

        cameraComboBox = new QComboBox(SensorBox);
        cameraComboBox->setObjectName(QStringLiteral("cameraComboBox"));

        horizontalLayout_5->addWidget(cameraComboBox);


        verticalLayout_3->addLayout(horizontalLayout_5);


        verticalLayout_6->addLayout(verticalLayout_3);

        cameraStackedWidget = new QStackedWidget(SensorBox);
        cameraStackedWidget->setObjectName(QStringLiteral("cameraStackedWidget"));
        page_12 = new QWidget();
        page_12->setObjectName(QStringLiteral("page_12"));
        gridLayout_11 = new QGridLayout(page_12);
        gridLayout_11->setSpacing(6);
        gridLayout_11->setContentsMargins(11, 11, 11, 11);
        gridLayout_11->setObjectName(QStringLiteral("gridLayout_11"));
        cameraLoadFileButton = new QPushButton(page_12);
        cameraLoadFileButton->setObjectName(QStringLiteral("cameraLoadFileButton"));

        gridLayout_11->addWidget(cameraLoadFileButton, 0, 0, 1, 1);

        cameraLoadedFileLabel = new QLabel(page_12);
        cameraLoadedFileLabel->setObjectName(QStringLiteral("cameraLoadedFileLabel"));

        gridLayout_11->addWidget(cameraLoadedFileLabel, 1, 0, 1, 1);

        gridLayout_9 = new QGridLayout();
        gridLayout_9->setSpacing(6);
        gridLayout_9->setObjectName(QStringLiteral("gridLayout_9"));
        gridLayout_9->setContentsMargins(-1, 0, -1, -1);
        resolutionyLabel = new QLabel(page_12);
        resolutionyLabel->setObjectName(QStringLiteral("resolutionyLabel"));

        gridLayout_9->addWidget(resolutionyLabel, 3, 0, 1, 1);

        resolutionxLabel = new QLabel(page_12);
        resolutionxLabel->setObjectName(QStringLiteral("resolutionxLabel"));

        gridLayout_9->addWidget(resolutionxLabel, 2, 0, 1, 1);

        pixelSizeLabel = new QLabel(page_12);
        pixelSizeLabel->setObjectName(QStringLiteral("pixelSizeLabel"));

        gridLayout_9->addWidget(pixelSizeLabel, 1, 0, 1, 1);

        pixelSizeUnitsLabel = new QLabel(page_12);
        pixelSizeUnitsLabel->setObjectName(QStringLiteral("pixelSizeUnitsLabel"));

        gridLayout_9->addWidget(pixelSizeUnitsLabel, 1, 2, 1, 1);

        pixelSizeValueLabel = new QLabel(page_12);
        pixelSizeValueLabel->setObjectName(QStringLiteral("pixelSizeValueLabel"));
        pixelSizeValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_9->addWidget(pixelSizeValueLabel, 1, 1, 1, 1);

        resolutionxValueLabel = new QLabel(page_12);
        resolutionxValueLabel->setObjectName(QStringLiteral("resolutionxValueLabel"));
        resolutionxValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_9->addWidget(resolutionxValueLabel, 2, 1, 1, 1);

        resolutionxUnitsLabel = new QLabel(page_12);
        resolutionxUnitsLabel->setObjectName(QStringLiteral("resolutionxUnitsLabel"));

        gridLayout_9->addWidget(resolutionxUnitsLabel, 2, 2, 1, 1);

        resolutionyValueLabel = new QLabel(page_12);
        resolutionyValueLabel->setObjectName(QStringLiteral("resolutionyValueLabel"));
        resolutionyValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_9->addWidget(resolutionyValueLabel, 3, 1, 1, 1);

        resolutionyUnitsLabel = new QLabel(page_12);
        resolutionyUnitsLabel->setObjectName(QStringLiteral("resolutionyUnitsLabel"));

        gridLayout_9->addWidget(resolutionyUnitsLabel, 3, 2, 1, 1);

        label_11 = new QLabel(page_12);
        label_11->setObjectName(QStringLiteral("label_11"));

        gridLayout_9->addWidget(label_11, 0, 0, 1, 1);

        sensorNameLabel = new QLabel(page_12);
        sensorNameLabel->setObjectName(QStringLiteral("sensorNameLabel"));
        sensorNameLabel->setAlignment(Qt::AlignCenter);

        gridLayout_9->addWidget(sensorNameLabel, 0, 1, 1, 1);


        gridLayout_11->addLayout(gridLayout_9, 2, 0, 1, 1);

        cameraStackedWidget->addWidget(page_12);
        page_13 = new QWidget();
        page_13->setObjectName(QStringLiteral("page_13"));
        cameraStackedWidget->addWidget(page_13);

        verticalLayout_6->addWidget(cameraStackedWidget);

        horizontalSpacer_3 = new QSpacerItem(287, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        verticalLayout_6->addItem(horizontalSpacer_3);


        horizontalLayout->addWidget(SensorBox);


        verticalLayout->addLayout(horizontalLayout);

        line_2 = new QFrame(centralWidget);
        line_2->setObjectName(QStringLiteral("line_2"));
        line_2->setFrameShape(QFrame::HLine);
        line_2->setFrameShadow(QFrame::Sunken);

        verticalLayout->addWidget(line_2);

        SceneBox = new QGroupBox(centralWidget);
        SceneBox->setObjectName(QStringLiteral("SceneBox"));
        gridLayout_3 = new QGridLayout(SceneBox);
        gridLayout_3->setSpacing(6);
        gridLayout_3->setContentsMargins(11, 11, 11, 11);
        gridLayout_3->setObjectName(QStringLiteral("gridLayout_3"));
        overlapValueLabel = new QLabel(SceneBox);
        overlapValueLabel->setObjectName(QStringLiteral("overlapValueLabel"));
        overlapValueLabel->setMinimumSize(QSize(25, 0));
        overlapValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_3->addWidget(overlapValueLabel, 1, 2, 1, 1);

        label_8 = new QLabel(SceneBox);
        label_8->setObjectName(QStringLiteral("label_8"));

        gridLayout_3->addWidget(label_8, 2, 0, 1, 1);

        altitudeLabel = new QLabel(SceneBox);
        altitudeLabel->setObjectName(QStringLiteral("altitudeLabel"));
        altitudeLabel->setMinimumSize(QSize(25, 0));
        altitudeLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_3->addWidget(altitudeLabel, 0, 2, 1, 1);

        label_7 = new QLabel(SceneBox);
        label_7->setObjectName(QStringLiteral("label_7"));

        gridLayout_3->addWidget(label_7, 1, 0, 1, 1);

        label_6 = new QLabel(SceneBox);
        label_6->setObjectName(QStringLiteral("label_6"));

        gridLayout_3->addWidget(label_6, 1, 5, 1, 1);

        label_5 = new QLabel(SceneBox);
        label_5->setObjectName(QStringLiteral("label_5"));

        gridLayout_3->addWidget(label_5, 2, 5, 1, 1);

        label_4 = new QLabel(SceneBox);
        label_4->setObjectName(QStringLiteral("label_4"));

        gridLayout_3->addWidget(label_4, 0, 0, 1, 1);

        overlapSlider = new QSlider(SceneBox);
        overlapSlider->setObjectName(QStringLiteral("overlapSlider"));
        overlapSlider->setOrientation(Qt::Horizontal);

        gridLayout_3->addWidget(overlapSlider, 1, 1, 1, 1);

        label_15 = new QLabel(SceneBox);
        label_15->setObjectName(QStringLiteral("label_15"));

        gridLayout_3->addWidget(label_15, 1, 3, 1, 1);

        speedValueLabel = new QLabel(SceneBox);
        speedValueLabel->setObjectName(QStringLiteral("speedValueLabel"));
        speedValueLabel->setMinimumSize(QSize(25, 0));
        speedValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_3->addWidget(speedValueLabel, 2, 2, 1, 1);

        speedUnitsLabel = new QLabel(SceneBox);
        speedUnitsLabel->setObjectName(QStringLiteral("speedUnitsLabel"));

        gridLayout_3->addWidget(speedUnitsLabel, 2, 3, 1, 1);

        speedSlider = new QSlider(SceneBox);
        speedSlider->setObjectName(QStringLiteral("speedSlider"));
        speedSlider->setMaximum(400);
        speedSlider->setOrientation(Qt::Horizontal);

        gridLayout_3->addWidget(speedSlider, 2, 1, 1, 1);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_2, 0, 4, 1, 1);

        altitudeUnitsLabel = new QLabel(SceneBox);
        altitudeUnitsLabel->setObjectName(QStringLiteral("altitudeUnitsLabel"));

        gridLayout_3->addWidget(altitudeUnitsLabel, 0, 3, 1, 1);

        bottomTypeCombo = new QComboBox(SceneBox);
        bottomTypeCombo->setObjectName(QStringLiteral("bottomTypeCombo"));

        gridLayout_3->addWidget(bottomTypeCombo, 2, 7, 1, 1);

        altitudeSlider = new QSlider(SceneBox);
        altitudeSlider->setObjectName(QStringLiteral("altitudeSlider"));
        altitudeSlider->setMaximum(1500);
        altitudeSlider->setSingleStep(0);
        altitudeSlider->setOrientation(Qt::Horizontal);

        gridLayout_3->addWidget(altitudeSlider, 0, 1, 1, 1);

        label_17 = new QLabel(SceneBox);
        label_17->setObjectName(QStringLiteral("label_17"));

        gridLayout_3->addWidget(label_17, 0, 5, 1, 1);

        dofUnitsLabel = new QLabel(SceneBox);
        dofUnitsLabel->setObjectName(QStringLiteral("dofUnitsLabel"));

        gridLayout_3->addWidget(dofUnitsLabel, 1, 9, 1, 1);

        dofValueLabel = new QLabel(SceneBox);
        dofValueLabel->setObjectName(QStringLiteral("dofValueLabel"));
        dofValueLabel->setMinimumSize(QSize(25, 0));
        dofValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_3->addWidget(dofValueLabel, 1, 8, 1, 1);

        motionBlurUnitsLabel = new QLabel(SceneBox);
        motionBlurUnitsLabel->setObjectName(QStringLiteral("motionBlurUnitsLabel"));

        gridLayout_3->addWidget(motionBlurUnitsLabel, 0, 9, 1, 1);

        motionBlurValueLabel = new QLabel(SceneBox);
        motionBlurValueLabel->setObjectName(QStringLiteral("motionBlurValueLabel"));
        motionBlurValueLabel->setMinimumSize(QSize(25, 0));
        motionBlurValueLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        gridLayout_3->addWidget(motionBlurValueLabel, 0, 8, 1, 1);

        motionBlurSlider = new QSlider(SceneBox);
        motionBlurSlider->setObjectName(QStringLiteral("motionBlurSlider"));
        motionBlurSlider->setOrientation(Qt::Horizontal);

        gridLayout_3->addWidget(motionBlurSlider, 0, 7, 1, 1);

        dofSlider = new QSlider(SceneBox);
        dofSlider->setObjectName(QStringLiteral("dofSlider"));
        dofSlider->setMaximum(600);
        dofSlider->setOrientation(Qt::Horizontal);

        gridLayout_3->addWidget(dofSlider, 1, 7, 1, 1);


        verticalLayout->addWidget(SceneBox);

        line_4 = new QFrame(centralWidget);
        line_4->setObjectName(QStringLiteral("line_4"));
        line_4->setFrameShape(QFrame::HLine);
        line_4->setFrameShadow(QFrame::Sunken);

        verticalLayout->addWidget(line_4);

        OutputBox = new QGroupBox(centralWidget);
        OutputBox->setObjectName(QStringLiteral("OutputBox"));
        gridLayout_4 = new QGridLayout(OutputBox);
        gridLayout_4->setSpacing(6);
        gridLayout_4->setContentsMargins(11, 11, 11, 11);
        gridLayout_4->setObjectName(QStringLiteral("gridLayout_4"));
        verticalSpacer_2 = new QSpacerItem(20, 15, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_4->addItem(verticalSpacer_2, 4, 0, 1, 1);

        FOVyLabel = new QLabel(OutputBox);
        FOVyLabel->setObjectName(QStringLiteral("FOVyLabel"));

        gridLayout_4->addWidget(FOVyLabel, 1, 0, 1, 1);

        FOVxLabel = new QLabel(OutputBox);
        FOVxLabel->setObjectName(QStringLiteral("FOVxLabel"));

        gridLayout_4->addWidget(FOVxLabel, 0, 0, 1, 1);

        apertureLabel = new QLabel(OutputBox);
        apertureLabel->setObjectName(QStringLiteral("apertureLabel"));

        gridLayout_4->addWidget(apertureLabel, 2, 0, 1, 1);

        exposureLabel = new QLabel(OutputBox);
        exposureLabel->setObjectName(QStringLiteral("exposureLabel"));

        gridLayout_4->addWidget(exposureLabel, 3, 0, 1, 1);


        verticalLayout->addWidget(OutputBox);

        line_5 = new QFrame(centralWidget);
        line_5->setObjectName(QStringLiteral("line_5"));
        line_5->setFrameShape(QFrame::HLine);
        line_5->setFrameShadow(QFrame::Sunken);

        verticalLayout->addWidget(line_5);

        horizontalLayout_7 = new QHBoxLayout();
        horizontalLayout_7->setSpacing(6);
        horizontalLayout_7->setObjectName(QStringLiteral("horizontalLayout_7"));
        horizontalLayout_7->setContentsMargins(-1, 0, -1, -1);
        saveButton = new QPushButton(centralWidget);
        saveButton->setObjectName(QStringLiteral("saveButton"));

        horizontalLayout_7->addWidget(saveButton);

        loadButton = new QPushButton(centralWidget);
        loadButton->setObjectName(QStringLiteral("loadButton"));

        horizontalLayout_7->addWidget(loadButton);

        exportButton = new QPushButton(centralWidget);
        exportButton->setObjectName(QStringLiteral("exportButton"));

        horizontalLayout_7->addWidget(exportButton);


        verticalLayout->addLayout(horizontalLayout_7);

        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1202, 25));
        menuUnderwater_Optical_Systems_Calculator = new QMenu(menuBar);
        menuUnderwater_Optical_Systems_Calculator->setObjectName(QStringLiteral("menuUnderwater_Optical_Systems_Calculator"));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        menuBar->addAction(menuUnderwater_Optical_Systems_Calculator->menuAction());

        retranslateUi(MainWindow);
        QObject::connect(LightsComboBox, SIGNAL(currentIndexChanged(int)), lightStackedWidget, SLOT(setCurrentIndex(int)));
        QObject::connect(LensComboBox, SIGNAL(currentIndexChanged(int)), lensStackedWidget, SLOT(setCurrentIndex(int)));
        QObject::connect(beamAngleSlider, SIGNAL(valueChanged(int)), beamAngleValueLabel, SLOT(setNum(int)));
        QObject::connect(altitudeSlider, SIGNAL(valueChanged(int)), altitudeLabel, SLOT(setNum(int)));
        QObject::connect(overlapSlider, SIGNAL(valueChanged(int)), overlapValueLabel, SLOT(setNum(int)));
        QObject::connect(motionBlurSlider, SIGNAL(valueChanged(int)), motionBlurValueLabel, SLOT(setNum(int)));
        QObject::connect(speedSlider, SIGNAL(valueChanged(int)), speedValueLabel, SLOT(setNum(int)));
        QObject::connect(dofSlider, SIGNAL(valueChanged(int)), dofValueLabel, SLOT(setNum(int)));
        QObject::connect(transmittanceSlider, SIGNAL(valueChanged(int)), transmittanceValueLabel, SLOT(setNum(int)));
        QObject::connect(focalLengthSlider, SIGNAL(valueChanged(int)), focalLengthSliderValueLabel, SLOT(setNum(int)));

        lightStackedWidget->setCurrentIndex(0);
        lensStackedWidget->setCurrentIndex(0);
        cameraStackedWidget->setCurrentIndex(0);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Underwater Optical Systems Calculator", 0));
        LightBox->setTitle(QApplication::translate("MainWindow", "Lights", 0));
        label->setText(QApplication::translate("MainWindow", "Light Type:", 0));
        LightsComboBox->clear();
        LightsComboBox->insertItems(0, QStringList()
         << QApplication::translate("MainWindow", "Custom", 0)
         << QApplication::translate("MainWindow", "Generic Led", 0)
         << QApplication::translate("MainWindow", "Generic Xenon", 0)
         << QApplication::translate("MainWindow", "Generic Tungsten", 0)
         << QApplication::translate("MainWindow", "Generic Halogen", 0)
        );
        lightsLoadFileButton->setText(QApplication::translate("MainWindow", "Load Light", 0));
        lightsLoadedFileLabel->setText(QApplication::translate("MainWindow", "No File Loaded", 0));
        label_21->setText(QApplication::translate("MainWindow", "LED", 0));
        label_3->setText(QApplication::translate("MainWindow", "Uses the spectral distribution of a generic white LED light.", 0));
        label_27->setText(QApplication::translate("MainWindow", "Xenon", 0));
        label_20->setText(QApplication::translate("MainWindow", "Tungsten", 0));
        label_28->setText(QApplication::translate("MainWindow", "Halogen", 0));
        luminousFluxLabel->setText(QApplication::translate("MainWindow", "Luminous flux", 0));
        beamAngleLabel->setText(QApplication::translate("MainWindow", "Beam Angle", 0));
        beamAngleValueLabel->setText(QApplication::translate("MainWindow", "15", 0));
        luminousFluxLineEdit->setText(QApplication::translate("MainWindow", "1000", 0));
        beamAngleUnitsLabel->setText(QApplication::translate("MainWindow", "deg", 0));
        liminousFluxUnitsLabel->setText(QApplication::translate("MainWindow", "lumen", 0));
        LensBox->setTitle(QApplication::translate("MainWindow", "Lens", 0));
        LensComboBox->clear();
        LensComboBox->insertItems(0, QStringList()
         << QApplication::translate("MainWindow", "Custom ", 0)
         << QApplication::translate("MainWindow", "Generic", 0)
        );
        label_2->setText(QApplication::translate("MainWindow", "Lens Type:", 0));
        lensLoadFileButton->setText(QApplication::translate("MainWindow", "Load Lens", 0));
        lensLoadedFileLabel->setText(QApplication::translate("MainWindow", "No File Loaded", 0));
        focalLengthLabel->setText(QApplication::translate("MainWindow", "Focal length:", 0));
        focalLengthValueLabel->setText(QApplication::translate("MainWindow", "0", 0));
        focalLengthUnitsLabel->setText(QApplication::translate("MainWindow", "mm", 0));
        label_32->setText(QApplication::translate("MainWindow", "Focal Length ", 0));
        label_34->setText(QApplication::translate("MainWindow", "Transmittance", 0));
        focalLenthSliderUnitsLabel->setText(QApplication::translate("MainWindow", "mm", 0));
        transmittanceValueLabel->setText(QApplication::translate("MainWindow", "90", 0));
        transmittanceUnitsLabel->setText(QApplication::translate("MainWindow", "%", 0));
        focalLengthSliderValueLabel->setText(QApplication::translate("MainWindow", "8", 0));
        SensorBox->setTitle(QApplication::translate("MainWindow", "Camera", 0));
        cameraTypeLabel->setText(QApplication::translate("MainWindow", "Camera Type:", 0));
        cameraComboBox->clear();
        cameraComboBox->insertItems(0, QStringList()
         << QApplication::translate("MainWindow", "Custom", 0)
        );
        cameraLoadFileButton->setText(QApplication::translate("MainWindow", "Load Camera", 0));
        cameraLoadedFileLabel->setText(QApplication::translate("MainWindow", "No File Loaded", 0));
        resolutionyLabel->setText(QApplication::translate("MainWindow", "Resolution y:", 0));
        resolutionxLabel->setText(QApplication::translate("MainWindow", "Resolution x:", 0));
        pixelSizeLabel->setText(QApplication::translate("MainWindow", "Pixel Size:", 0));
        pixelSizeUnitsLabel->setText(QApplication::translate("MainWindow", "um", 0));
        pixelSizeValueLabel->setText(QApplication::translate("MainWindow", "0", 0));
        resolutionxValueLabel->setText(QApplication::translate("MainWindow", "0", 0));
        resolutionxUnitsLabel->setText(QApplication::translate("MainWindow", "px", 0));
        resolutionyValueLabel->setText(QApplication::translate("MainWindow", "0", 0));
        resolutionyUnitsLabel->setText(QApplication::translate("MainWindow", "px", 0));
        label_11->setText(QApplication::translate("MainWindow", "Sensor", 0));
        sensorNameLabel->setText(QApplication::translate("MainWindow", "-", 0));
        SceneBox->setTitle(QApplication::translate("MainWindow", "Scene / Operational Parameters", 0));
        overlapValueLabel->setText(QApplication::translate("MainWindow", "0", 0));
        label_8->setText(QApplication::translate("MainWindow", "Speed", 0));
        altitudeLabel->setText(QApplication::translate("MainWindow", "0", 0));
        label_7->setText(QApplication::translate("MainWindow", "Overlap", 0));
        label_6->setText(QApplication::translate("MainWindow", "Depth of Field", 0));
        label_5->setText(QApplication::translate("MainWindow", "Bottom Type", 0));
        label_4->setText(QApplication::translate("MainWindow", "Altitude", 0));
        label_15->setText(QApplication::translate("MainWindow", "%", 0));
        speedValueLabel->setText(QApplication::translate("MainWindow", "1", 0));
        speedUnitsLabel->setText(QApplication::translate("MainWindow", "cm/s", 0));
        altitudeUnitsLabel->setText(QApplication::translate("MainWindow", "cm", 0));
        bottomTypeCombo->clear();
        bottomTypeCombo->insertItems(0, QStringList()
         << QApplication::translate("MainWindow", "Sand", 0)
         << QApplication::translate("MainWindow", "Custom", 0)
         << QApplication::translate("MainWindow", "Algae", 0)
         << QApplication::translate("MainWindow", "Coral", 0)
         << QApplication::translate("MainWindow", "Rock", 0)
        );
        label_17->setText(QApplication::translate("MainWindow", "Max Motion Blur", 0));
        dofUnitsLabel->setText(QApplication::translate("MainWindow", "cm", 0));
        dofValueLabel->setText(QApplication::translate("MainWindow", "1", 0));
        motionBlurUnitsLabel->setText(QApplication::translate("MainWindow", "pixel", 0));
        motionBlurValueLabel->setText(QApplication::translate("MainWindow", "2", 0));
        OutputBox->setTitle(QApplication::translate("MainWindow", "Output", 0));
        FOVyLabel->setText(QApplication::translate("MainWindow", "FOV_y", 0));
        FOVxLabel->setText(QApplication::translate("MainWindow", "FOV_x", 0));
        apertureLabel->setText(QApplication::translate("MainWindow", "Aperture", 0));
        exposureLabel->setText(QApplication::translate("MainWindow", "Exposure", 0));
        saveButton->setText(QApplication::translate("MainWindow", "Save Configuration", 0));
        loadButton->setText(QApplication::translate("MainWindow", "Load Configuration", 0));
        exportButton->setText(QApplication::translate("MainWindow", "Export Report", 0));
        menuUnderwater_Optical_Systems_Calculator->setTitle(QApplication::translate("MainWindow", "Underwater Optical Systems Calculator", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
