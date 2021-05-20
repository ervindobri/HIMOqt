import myo
from PyQt6 import QtCore
from PyQt6.QtCore import QThread


class SessionThread(QThread):
    exerciseResult = QtCore.pyqtSignal(str)

    def __init__(self, classification, parent=None):
        QThread.__init__(self, parent)
        self.classification = classification
        self.classification.hub = myo.Hub()

    def run(self):
        exists = self.classification.model_exists()
        while exists:
            res = self.classification.Predict()
            print(res)
            self.exerciseResult.emit(res)

