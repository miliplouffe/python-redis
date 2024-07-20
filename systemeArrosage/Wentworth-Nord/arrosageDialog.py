# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog2.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHeaderView, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QTableWidget,
    QTableWidgetItem, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1158, 673)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(370, 0, 371, 41))
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(40, 70, 431, 221))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(16)
        font1.setBold(False)
        font1.setItalic(False)
        self.groupBox.setFont(font1)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
"	font: 16pt \"MS Shell Dlg 2\";\n"
"	border-color: rgb(48, 48, 48);\n"
"    background-color: rgb(255, 230, 205);\n"
"    margin-top:1em;\n"
"}\n"
"QGroupBox QGroupBox {\n"
"    background-color: green;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: left top;\n"
"    background: transparent;\n"
"    margin-top: -2.5em;\n"
"}")
        self.groupBox.setFlat(False)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 90, 161, 16))
        font2 = QFont()
        self.label_2.setFont(font2)
        self.DetecteurPluieActif = QCheckBox(self.groupBox)
        self.DetecteurPluieActif.setObjectName(u"DetecteurPluieActif")
        self.DetecteurPluieActif.setGeometry(QRect(200, 90, 21, 21))
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 120, 161, 16))
        self.label_3.setFont(font2)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 60, 161, 16))
        self.label_4.setFont(font2)
        self.ArrosageActif = QCheckBox(self.groupBox)
        self.ArrosageActif.setObjectName(u"ArrosageActif")
        self.ArrosageActif.setGeometry(QRect(200, 60, 21, 21))
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 150, 161, 16))
        self.label_5.setFont(font2)
        self.HeureArrosage = QSpinBox(self.groupBox)
        self.HeureArrosage.setObjectName(u"HeureArrosage")
        self.HeureArrosage.setGeometry(QRect(200, 150, 42, 22))
        self.HeureArrosage.setMinimum(1)
        self.HeureArrosage.setMaximum(24)
        self.JourArrosage = QComboBox(self.groupBox)
        self.JourArrosage.addItem("")
        self.JourArrosage.addItem("")
        self.JourArrosage.setObjectName(u"JourArrosage")
        self.JourArrosage.setGeometry(QRect(200, 120, 131, 22))
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 180, 171, 16))
        self.label_6.setFont(font2)
        self.IntervalEntreArrosage = QSpinBox(self.groupBox)
        self.IntervalEntreArrosage.setObjectName(u"IntervalEntreArrosage")
        self.IntervalEntreArrosage.setGeometry(QRect(200, 180, 42, 22))
        self.IntervalEntreArrosage.setMinimum(0)
        self.IntervalEntreArrosage.setMaximum(7)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(40, 320, 241, 281))
        self.groupBox_2.setFont(font1)
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
"	font: 16pt \"MS Shell Dlg 2\";\n"
"	border-color: rgb(48, 48, 48);\n"
"    background-color: rgb(255, 230, 205);\n"
"    margin-top:1em;\n"
"}\n"
"QGroupBox QGroupBox {\n"
"    background-color: green;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: left top;\n"
"    background: transparent;\n"
"    margin-top: -2.5em;\n"
"}")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 130, 101, 16))
        font3 = QFont()
        font3.setPointSize(12)
        self.label_7.setFont(font3)
        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 160, 141, 16))
        self.label_8.setFont(font3)
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 190, 141, 16))
        self.label_9.setFont(font3)
        self.Zone1TempsArrosage = QSpinBox(self.groupBox_2)
        self.Zone1TempsArrosage.setObjectName(u"Zone1TempsArrosage")
        self.Zone1TempsArrosage.setGeometry(QRect(170, 160, 42, 22))
        self.Zone1TempsArrosage.setMinimum(1)
        self.Zone1TempsArrosage.setMaximum(60)
        self.Zone1Active = QCheckBox(self.groupBox_2)
        self.Zone1Active.setObjectName(u"Zone1Active")
        self.Zone1Active.setGeometry(QRect(110, 130, 21, 21))
        self.Zone1Physique = QTextEdit(self.groupBox_2)
        self.Zone1Physique.setObjectName(u"Zone1Physique")
        self.Zone1Physique.setGeometry(QRect(10, 220, 211, 51))
        font4 = QFont()
        font4.setFamilies([u"MS Sans Serif"])
        font4.setPointSize(12)
        self.Zone1Physique.setFont(font4)
        self.Zone1Physique.setLineWrapColumnOrWidth(-3)
        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(10, 40, 51, 16))
        self.label_19.setFont(font3)
        self.NoZone1 = QLabel(self.groupBox_2)
        self.NoZone1.setObjectName(u"NoZone1")
        self.NoZone1.setGeometry(QRect(60, 40, 31, 21))
        self.NoZone1.setFont(font3)
        self.OuvMan1 = QPushButton(self.groupBox_2)
        self.OuvMan1.setObjectName(u"OuvMan1")
        self.OuvMan1.setGeometry(QRect(70, 80, 21, 23))
        self.FermMan1 = QPushButton(self.groupBox_2)
        self.FermMan1.setObjectName(u"FermMan1")
        self.FermMan1.setGeometry(QRect(100, 80, 21, 23))
        self.label_27 = QLabel(self.groupBox_2)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(10, 80, 61, 16))
        self.label_27.setFont(font3)
        self.label_31 = QLabel(self.groupBox_2)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setGeometry(QRect(130, 60, 101, 16))
        font5 = QFont()
        font5.setPointSize(10)
        self.label_31.setFont(font5)
        self.GicleurSet1 = QPushButton(self.groupBox_2)
        self.GicleurSet1.setObjectName(u"GicleurSet1")
        self.GicleurSet1.setGeometry(QRect(150, 80, 21, 23))
        self.GicleurReSet1 = QPushButton(self.groupBox_2)
        self.GicleurReSet1.setObjectName(u"GicleurReSet1")
        self.GicleurReSet1.setGeometry(QRect(180, 80, 21, 23))
        self.OuvMan1_4 = QPushButton(self.groupBox_2)
        self.OuvMan1_4.setObjectName(u"OuvMan1_4")
        self.OuvMan1_4.setGeometry(QRect(280, 120, 21, 23))
        self.OuvMan1_5 = QPushButton(self.groupBox_2)
        self.OuvMan1_5.setObjectName(u"OuvMan1_5")
        self.OuvMan1_5.setGeometry(QRect(250, 120, 21, 23))
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(310, 320, 241, 281))
        self.groupBox_3.setFont(font1)
        self.groupBox_3.setStyleSheet(u"QGroupBox {\n"
"	font: 16pt \"MS Shell Dlg 2\";\n"
"	border-color: rgb(48, 48, 48);\n"
"    background-color: rgb(255, 230, 205);\n"
"    margin-top:1em;\n"
"}\n"
"QGroupBox QGroupBox {\n"
"    background-color: green;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: left top;\n"
"    background: transparent;\n"
"    margin-top: -2.5em;\n"
"}")
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 130, 101, 16))
        self.label_10.setFont(font3)
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 160, 141, 16))
        self.label_11.setFont(font3)
        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 190, 141, 16))
        self.label_12.setFont(font3)
        self.Zone2TempsArrosage = QSpinBox(self.groupBox_3)
        self.Zone2TempsArrosage.setObjectName(u"Zone2TempsArrosage")
        self.Zone2TempsArrosage.setGeometry(QRect(170, 160, 42, 22))
        self.Zone2TempsArrosage.setMinimum(1)
        self.Zone2TempsArrosage.setMaximum(60)
        self.Zone2Active = QCheckBox(self.groupBox_3)
        self.Zone2Active.setObjectName(u"Zone2Active")
        self.Zone2Active.setGeometry(QRect(110, 130, 21, 21))
        self.Zone2Physique = QTextEdit(self.groupBox_3)
        self.Zone2Physique.setObjectName(u"Zone2Physique")
        self.Zone2Physique.setGeometry(QRect(10, 220, 211, 51))
        self.Zone2Physique.setFont(font4)
        self.Zone2Physique.setLineWrapColumnOrWidth(-3)
        self.label_24 = QLabel(self.groupBox_3)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(10, 40, 51, 16))
        self.label_24.setFont(font3)
        self.NoZone2 = QLabel(self.groupBox_3)
        self.NoZone2.setObjectName(u"NoZone2")
        self.NoZone2.setGeometry(QRect(60, 40, 31, 21))
        self.NoZone2.setFont(font3)
        self.OuvMan2 = QPushButton(self.groupBox_3)
        self.OuvMan2.setObjectName(u"OuvMan2")
        self.OuvMan2.setGeometry(QRect(70, 80, 21, 23))
        self.FermMan2 = QPushButton(self.groupBox_3)
        self.FermMan2.setObjectName(u"FermMan2")
        self.FermMan2.setGeometry(QRect(100, 80, 21, 23))
        self.label_28 = QLabel(self.groupBox_3)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(10, 80, 61, 16))
        self.label_28.setFont(font3)
        self.label_32 = QLabel(self.groupBox_3)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setGeometry(QRect(130, 60, 101, 16))
        self.label_32.setFont(font5)
        self.GicleurSet2 = QPushButton(self.groupBox_3)
        self.GicleurSet2.setObjectName(u"GicleurSet2")
        self.GicleurSet2.setGeometry(QRect(150, 80, 21, 23))
        self.GicleurReSet2 = QPushButton(self.groupBox_3)
        self.GicleurReSet2.setObjectName(u"GicleurReSet2")
        self.GicleurReSet2.setGeometry(QRect(180, 80, 21, 23))
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(570, 320, 241, 281))
        self.groupBox_4.setFont(font1)
        self.groupBox_4.setStyleSheet(u"QGroupBox {\n"
"	font: 16pt \"MS Shell Dlg 2\";\n"
"	border-color: rgb(48, 48, 48);\n"
"    background-color: rgb(255, 230, 205);\n"
"    margin-top:1em;\n"
"}\n"
"QGroupBox QGroupBox {\n"
"    background-color: green;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: left top;\n"
"    background: transparent;\n"
"    margin-top: -2.5em;\n"
"}")
        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(20, 130, 101, 16))
        self.label_13.setFont(font3)
        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(20, 160, 141, 16))
        self.label_14.setFont(font3)
        self.label_15 = QLabel(self.groupBox_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(20, 190, 141, 16))
        self.label_15.setFont(font3)
        self.Zone3TempsArrosage = QSpinBox(self.groupBox_4)
        self.Zone3TempsArrosage.setObjectName(u"Zone3TempsArrosage")
        self.Zone3TempsArrosage.setGeometry(QRect(180, 160, 42, 22))
        self.Zone3TempsArrosage.setMinimum(1)
        self.Zone3TempsArrosage.setMaximum(60)
        self.Zone3Active = QCheckBox(self.groupBox_4)
        self.Zone3Active.setObjectName(u"Zone3Active")
        self.Zone3Active.setGeometry(QRect(120, 130, 21, 21))
        self.Zone3Physique = QTextEdit(self.groupBox_4)
        self.Zone3Physique.setObjectName(u"Zone3Physique")
        self.Zone3Physique.setGeometry(QRect(20, 220, 211, 51))
        self.Zone3Physique.setFont(font4)
        self.Zone3Physique.setLineWrapColumnOrWidth(-3)
        self.label_25 = QLabel(self.groupBox_4)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(10, 40, 51, 16))
        self.label_25.setFont(font3)
        self.NoZone3 = QLabel(self.groupBox_4)
        self.NoZone3.setObjectName(u"NoZone3")
        self.NoZone3.setGeometry(QRect(70, 40, 31, 21))
        self.NoZone3.setFont(font3)
        self.OuvMan3 = QPushButton(self.groupBox_4)
        self.OuvMan3.setObjectName(u"OuvMan3")
        self.OuvMan3.setGeometry(QRect(80, 80, 21, 23))
        self.FermMan3 = QPushButton(self.groupBox_4)
        self.FermMan3.setObjectName(u"FermMan3")
        self.FermMan3.setGeometry(QRect(110, 80, 21, 23))
        self.label_33 = QLabel(self.groupBox_4)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setGeometry(QRect(20, 80, 61, 16))
        self.label_33.setFont(font3)
        self.GicleurReSet3 = QPushButton(self.groupBox_4)
        self.GicleurReSet3.setObjectName(u"GicleurReSet3")
        self.GicleurReSet3.setGeometry(QRect(180, 80, 21, 23))
        self.GicleurSet3 = QPushButton(self.groupBox_4)
        self.GicleurSet3.setObjectName(u"GicleurSet3")
        self.GicleurSet3.setGeometry(QRect(150, 80, 21, 23))
        self.label_34 = QLabel(self.groupBox_4)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setGeometry(QRect(130, 60, 101, 16))
        self.label_34.setFont(font5)
        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(830, 320, 241, 281))
        self.groupBox_5.setFont(font1)
        self.groupBox_5.setStyleSheet(u"QGroupBox {\n"
"	font: 16pt \"MS Shell Dlg 2\";\n"
"	border-color: rgb(48, 48, 48);\n"
"    background-color: rgb(255, 230, 205);\n"
"    margin-top:1em;\n"
"}\n"
"QGroupBox QGroupBox {\n"
"    background-color: green;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: left top;\n"
"    background: transparent;\n"
"    margin-top: -2.5em;\n"
"}")
        self.label_16 = QLabel(self.groupBox_5)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(20, 130, 101, 16))
        self.label_16.setFont(font3)
        self.label_17 = QLabel(self.groupBox_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(20, 160, 141, 16))
        self.label_17.setFont(font3)
        self.label_18 = QLabel(self.groupBox_5)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(20, 190, 141, 16))
        self.label_18.setFont(font3)
        self.Zone4TempsArrosage = QSpinBox(self.groupBox_5)
        self.Zone4TempsArrosage.setObjectName(u"Zone4TempsArrosage")
        self.Zone4TempsArrosage.setGeometry(QRect(180, 160, 42, 22))
        self.Zone4TempsArrosage.setMinimum(1)
        self.Zone4TempsArrosage.setMaximum(60)
        self.Zone4Active = QCheckBox(self.groupBox_5)
        self.Zone4Active.setObjectName(u"Zone4Active")
        self.Zone4Active.setGeometry(QRect(120, 130, 21, 21))
        self.Zone4Physique = QTextEdit(self.groupBox_5)
        self.Zone4Physique.setObjectName(u"Zone4Physique")
        self.Zone4Physique.setGeometry(QRect(20, 220, 211, 51))
        self.Zone4Physique.setFont(font4)
        self.Zone4Physique.setLineWrapColumnOrWidth(-3)
        self.label_26 = QLabel(self.groupBox_5)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(10, 40, 41, 16))
        self.label_26.setFont(font3)
        self.NoZone4 = QLabel(self.groupBox_5)
        self.NoZone4.setObjectName(u"NoZone4")
        self.NoZone4.setGeometry(QRect(50, 40, 31, 21))
        self.NoZone4.setFont(font3)
        self.OuvMan4 = QPushButton(self.groupBox_5)
        self.OuvMan4.setObjectName(u"OuvMan4")
        self.OuvMan4.setGeometry(QRect(80, 80, 21, 23))
        self.FermMan4 = QPushButton(self.groupBox_5)
        self.FermMan4.setObjectName(u"FermMan4")
        self.FermMan4.setGeometry(QRect(110, 80, 21, 23))
        self.label_35 = QLabel(self.groupBox_5)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setGeometry(QRect(20, 80, 61, 16))
        self.label_35.setFont(font3)
        self.label_36 = QLabel(self.groupBox_5)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setGeometry(QRect(130, 60, 101, 16))
        self.label_36.setFont(font5)
        self.GicleurReSet4 = QPushButton(self.groupBox_5)
        self.GicleurReSet4.setObjectName(u"GicleurReSet4")
        self.GicleurReSet4.setGeometry(QRect(180, 80, 21, 23))
        self.GicleurSet4 = QPushButton(self.groupBox_5)
        self.GicleurSet4.setObjectName(u"GicleurSet4")
        self.GicleurSet4.setGeometry(QRect(150, 80, 21, 23))
        self.Sauvegarde = QPushButton(self.centralwidget)
        self.Sauvegarde.setObjectName(u"Sauvegarde")
        self.Sauvegarde.setGeometry(QRect(540, 110, 211, 61))
        self.Sauvegarde.setFont(font3)
        self.Sauvegarde.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.Reinitialiser = QPushButton(self.centralwidget)
        self.Reinitialiser.setObjectName(u"Reinitialiser")
        self.Reinitialiser.setGeometry(QRect(540, 190, 211, 61))
        self.Reinitialiser.setFont(font3)
        self.Reinitialiser.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.OuvrirMessage = QPushButton(self.centralwidget)
        self.OuvrirMessage.setObjectName(u"OuvrirMessage")
        self.OuvrirMessage.setGeometry(QRect(880, 110, 211, 61))
        self.OuvrirMessage.setFont(font3)
        self.OuvrirMessage.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.FermerMessage = QPushButton(self.centralwidget)
        self.FermerMessage.setObjectName(u"FermerMessage")
        self.FermerMessage.setGeometry(QRect(880, 190, 211, 61))
        self.FermerMessage.setFont(font3)
        self.FermerMessage.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.Logs = QTableWidget(self.centralwidget)
        if (self.Logs.columnCount() < 3):
            self.Logs.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font3);
        self.Logs.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font3);
        self.Logs.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font3);
        self.Logs.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.Logs.setObjectName(u"Logs")
        self.Logs.setGeometry(QRect(20, 60, 811, 261))
        self.Logs.setAutoFillBackground(False)
        self.Logs.setStyleSheet(u"\n"
"\n"
"QTableView {\n"
"    background-color: rgb(255, 230, 205);\n"
"    gridline-color: black;\n"
"    border-color: rgb(242, 128, 133);\n"
"    font: 12px;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: rgb(24, 125, 19);\n"
"    color: white;\n"
"    height: 35px;\n"
"    font: 14px;\n"
"}\n"
"QTableView::item:focus{\n"
"    border: 2px solid rgb(242, 128, 133);\n"
"    background-color: rgb(255, 254, 229);\n"
"}\n"
"QScrollBar:vertical {\n"
"    background: rgb(188, 224, 235);\n"
"}\n"
" QScrollBar::handle:vertical {\n"
"    background: rgb(71, 153, 176);\n"
" }\n"
"QScrollBar:horizontal {\n"
"    background: rgb(188, 224, 235);\n"
"}\n"
" QScrollBar::handle:horizontal {\n"
"    background: rgb(71, 153, 176);\n"
" }\n"
"\n"
"")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Syst\u00e8me d'arrosage Montr\u00e9al", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Syst\u00e8me g\u00e9n\u00e9ral", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"D\u00e9tecteur pluie actif", None))
        self.DetecteurPluieActif.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Jour d'arrosage", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Syst\u00e8me arrosage actif", None))
        self.ArrosageActif.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Heure d'arrosage", None))
        self.JourArrosage.setItemText(0, QCoreApplication.translate("MainWindow", u"Pair", None))
        self.JourArrosage.setItemText(1, QCoreApplication.translate("MainWindow", u"Impair", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Interval jours arrosage", None))
        self.groupBox_2.setTitle("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Zone active", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Temps d'arrosage", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Zone d'arrosage", None))
        self.Zone1Active.setText("")
        self.Zone1Physique.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Sans Serif'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:11pt;\">Avant de la maison au bord de la rue</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:11pt;\"><br /></p></body></html>", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Zone", None))
        self.NoZone1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.OuvMan1.setText(QCoreApplication.translate("MainWindow", u"O", None))
        self.FermMan1.setText(QCoreApplication.translate("MainWindow", u"F", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Manuel", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Syst\u00e8me Gicleurs", None))
        self.GicleurSet1.setText(QCoreApplication.translate("MainWindow", u"S", None))
        self.GicleurReSet1.setText(QCoreApplication.translate("MainWindow", u"R", None))
        self.OuvMan1_4.setText(QCoreApplication.translate("MainWindow", u"R", None))
        self.OuvMan1_5.setText(QCoreApplication.translate("MainWindow", u"S", None))
        self.groupBox_3.setTitle("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Zone active", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Temps d'arrosage", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Zone d'arrosage", None))
        self.Zone2Active.setText("")
        self.Zone2Physique.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Sans Serif'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:11pt;\">Avant pr\u00e8s de la maison</span></p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Zone", None))
        self.NoZone2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.OuvMan2.setText(QCoreApplication.translate("MainWindow", u"O", None))
        self.FermMan2.setText(QCoreApplication.translate("MainWindow", u"F", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Manuel", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Syst\u00e8me Gicleurs", None))
        self.GicleurSet2.setText(QCoreApplication.translate("MainWindow", u"S", None))
        self.GicleurReSet2.setText(QCoreApplication.translate("MainWindow", u"R", None))
        self.groupBox_4.setTitle("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Zone active", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Temps d'arrosage", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Zone d'arrosage", None))
        self.Zone3Active.setText("")
        self.Zone3Physique.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Sans Serif'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:11pt;\">Cot\u00e9 de la maison</span></p></body></html>", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Zone", None))
        self.NoZone3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.OuvMan3.setText(QCoreApplication.translate("MainWindow", u"O", None))
        self.FermMan3.setText(QCoreApplication.translate("MainWindow", u"F", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Manuel", None))
        self.GicleurReSet3.setText(QCoreApplication.translate("MainWindow", u"R", None))
        self.GicleurSet3.setText(QCoreApplication.translate("MainWindow", u"S", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Syst\u00e8me Gicleurs", None))
        self.groupBox_5.setTitle("")
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Zone active", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Temps d'arrosage", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Zone d'arrosage", None))
        self.Zone4Active.setText("")
        self.Zone4Physique.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Sans Serif'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:11pt;\">Arri\u00e8re de la maison</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:11pt;\"><br /></p></body></html>", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Zone", None))
        self.NoZone4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.OuvMan4.setText(QCoreApplication.translate("MainWindow", u"O", None))
        self.FermMan4.setText(QCoreApplication.translate("MainWindow", u"F", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Manuel", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Syst\u00e8me Gicleurs", None))
        self.GicleurReSet4.setText(QCoreApplication.translate("MainWindow", u"R", None))
        self.GicleurSet4.setText(QCoreApplication.translate("MainWindow", u"S", None))
        self.Sauvegarde.setText(QCoreApplication.translate("MainWindow", u"Sauvegarde les donn\u00e9es", None))
        self.Reinitialiser.setText(QCoreApplication.translate("MainWindow", u"R\u00e9initialiser les donn\u00e9es", None))
        self.OuvrirMessage.setText(QCoreApplication.translate("MainWindow", u"Ouvrir les messages", None))
        self.FermerMessage.setText(QCoreApplication.translate("MainWindow", u"Fermer les messages", None))
        ___qtablewidgetitem = self.Logs.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Date", None));
        ___qtablewidgetitem1 = self.Logs.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Zone", None));
        ___qtablewidgetitem2 = self.Logs.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Message", None));
    # retranslateUi

