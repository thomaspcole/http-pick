from PyQt5.QtWidgets import (QGridLayout, QLabel, QMainWindow, QPushButton, QSizePolicy, QSlider, QSpinBox, QToolButton, QVBoxLayout, QWidget, QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from http_pick.util import getInstalledBrowsers

class SettingsWindow(QMainWindow):
    def __init__(self, iconsize):
        super().__init__()
        self.currentPx = 16

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.lay = QGridLayout(self.centralWidget)

        self.lbl = QLabel()
        self.lbl.setText("------ Settings ------")
        self.lay.addWidget(self.lbl,1,1,1,2, QtCore.Qt.AlignCenter)

        #Show detected web browsers
        self.lbl = QLabel()
        self.lbl.setText("Detected Web Browsers: ")
        self.lay.addWidget(self.lbl, 2,1,QtCore.Qt.AlignCenter)

        self.vbox = QVBoxLayout()
        self.refreshBrowsers()            
        self.lay.addLayout(self.vbox, 2, 2)

        #Refresh button
        self.btn = QPushButton()
        self.btn.setText("Refresh browser list.")
        self.btn.clicked.connect(lambda v: self.refreshBrowsers())
        self.lay.addWidget(self.btn, 3, 1, 1, 2)

        self.lbl = QLabel()
        self.lbl.setText("Icon Size: ")
        self.lay.addWidget(self.lbl,4,1,QtCore.Qt.AlignCenter)

        self.sliderBox = QVBoxLayout()

        self.icon = QToolButton(self) 
        self.icon.setIcon(QIcon.fromTheme('emblem-system'))
        self.icon.setText("Current Size: %spx" % (self.currentPx))
        self.icon.setIconSize(QtCore.QSize(self.currentPx, self.currentPx))
        self.icon.setStyleSheet("QToolButton {background-color: transparent; border: 0px; color: black;}")
        self.icon.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon) 
        self.icon.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed))
        self.sliderBox.addWidget(self.icon)

        self.isl = QSlider(QtCore.Qt.Horizontal)
        self.isl.setTickPosition(QSlider.TicksBelow)
        self.isl.setTickInterval(1)
        self.isl.setRange(1, 6)
        self.isl.valueChanged.connect(self.sliderValChanged)
        self.sliderBox.addWidget(self.isl)

        self.lay.addLayout(self.sliderBox, 4, 2)

    def sliderValChanged(self):
        self.currentPx = self.isl.value()*16
        self.icon.setText("Current Size: %spx" % (self.currentPx))
        self.icon.setIconSize(QtCore.QSize(self.currentPx, self.currentPx))
        self.icon.updateGeometry()




    def refreshBrowsers(self):
        #Clear existing widgets
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)

        #Build new widgets
        for b in getInstalledBrowsers():
            self.btn = QToolButton(self)  
            if '/' in b: #'Normal' launch path
                path = b
                appname = path.split('/')
            elif '.' in b: #Flatpak ref
                path = b
                appname = path.split('.')
            self.btn.setIcon(QIcon.fromTheme(appname[-1]))
            self.btn.setIconSize(QtCore.QSize(24,24))
            self.btn.setStyleSheet("QToolButton {background-color: transparent; border: 0px; color: black;}")
            self.btn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)          
            self.btn.setText(appname[-1].capitalize())
            self.btn.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,  QSizePolicy.Fixed))
            self.vbox.addWidget(self.btn)
