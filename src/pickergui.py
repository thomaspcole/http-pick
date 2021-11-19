from PyQt5.QtWidgets import (QMainWindow, QToolButton, QWidget, QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from math import floor
import sys

class MainWindow(QMainWindow): 
    def __init__(self, browsers, iconsize=72, displayappname=False, x=0, y=0, callback=lambda v: print(v)):                                         
        super().__init__()
        self.setFocus()

        self.centralwidget = QWidget()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setCentralWidget(self.centralwidget)
        self.lay = QHBoxLayout(self.centralwidget)
        self.lay.setContentsMargins(0,0,0,0)
        self.lay.setSpacing(0)

        xOffset = floor((iconsize*len(browsers))/2)
        yOffset = floor(iconsize*1.25)

        self.move(x-xOffset,y-yOffset)

        for b in browsers:                                          
            self.btn = QToolButton(self)  
            if '/' in b: #'Normal' launch path
                path = b
                appname = path.split('/')
            elif '.' in b: #Flatpak ref
                path = b
                appname = path.split('.')
            self.btn.setIcon(QIcon.fromTheme(appname[-1]))
            self.btn.setIconSize(QtCore.QSize(iconsize,iconsize))
            self.btn.setStyleSheet("QToolButton {background-color: transparent; border: 0px; color: white;}")

            if(displayappname):
                self.btn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)          
                self.btn.setText(appname[-1].capitalize())

            self.btn.clicked.connect(lambda v, path=path : callback(path))
            self.lay.addWidget(self.btn)
    
    def on_focusChanged(self):
        if(self.isActiveWindow() == False):
            sys.exit(0)