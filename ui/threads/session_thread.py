import time

import myo
from PyQt6 import QtCore
from PyQt6.QtCore import QThread


class SessionThread(QThread):
    exerciseResult = QtCore.pyqtSignal(str)
    exists = QtCore.pyqtSignal(bool)

    def __init__(self, classification, parent=None):
        QThread.__init__(self, parent)
        self.classification = classification
        self.classification.hub = myo.Hub()
        self.holding = False

    def run(self):
        exists = self.classification.model_exists()
        self.exists.emit(exists)
        while exists:
            res = self.classification.Predict(self.holding)
            print(res)
            self.exerciseResult.emit(res)
            time.sleep(0.1)

