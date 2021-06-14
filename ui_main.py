import os
import sys

from PyQt6 import QtGui
from PyQt6.QtGui import QIcon

import myo
from PyQt6.QtWidgets import QMainWindow, QApplication
from ui.main_widget import MainWidget
from ui.widgets.dialogs.tutorial_dialog import TutorialDialog


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
        self.createMenuBar()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumHeight(self.height)
        self.setMinimumWidth(self.width)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setCentralWidget(self.mainWidget)
        self.setMinimumSize(700, 400)
        self.show()



    def createMenuBar(self):
        menuBar = self.menuBar()
        # Help menu
        helpMenu = menuBar.addMenu(QIcon(":help-content.svg"), "&Help")
        helpContentAction = QtGui.QAction("Usage", self)
        helpContentAction.setShortcut("Ctrl+U")
        helpContentAction.setStatusTip('How to use the application?')
        helpContentAction.triggered.connect(self.appTutorial)

        aboutAction = QtGui.QAction("About", self)
        aboutAction.triggered.connect(self.appAbout)

        helpMenu.addAction(helpContentAction)
        helpMenu.addAction(aboutAction)


    def appAbout(self):
        print("About")

    def appTutorial(self):
        print("Tutorial")
        dialog = TutorialDialog(self)
        dialog.exec()

def main():
    myo.init(sdk_path=os.getcwd())
    app = QApplication(sys.argv)
    ex = HIMOApp()
    app.exec()
