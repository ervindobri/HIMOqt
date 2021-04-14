import os
import sys
import time

import myo
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QPushButton, QLabel, QWidget, QHBoxLayout, QStyle, QApplication
import classification as clf
from constants import PREDEFINED_EXERCISES
from ui.main_widget import MainWidget


class HIMOApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = int(self.screen().size().width() / 4)
        self.top = int(self.screen().size().height() / 4)
        self.width = 600
        self.height = 350

        self.title = 'HIMO - Health In MOtion'
        self.mainWidget = MainWidget(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumHeight(self.height)
        self.setMinimumWidth(self.width)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setCentralWidget(self.mainWidget)
        self.setMinimumSize(700, 400)

        self.show()


if __name__ == '__main__':
    myo.init(sdk_path=os.getcwd())
    app = QApplication(sys.argv)
    ex = HIMOApp()
    app.exec_()