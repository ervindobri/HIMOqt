from PyQt6 import QtCore
from PyQt6.QtCore import QThread

from helpers.classification import Classification


class TrainThread(QThread):
    taskFinished = QtCore.pyqtSignal()


    def __init__(self,
                 classify: Classification = None,
                 exercise: str = None
                 ):
        QThread.__init__(self)
        self.classify = classify
        self.exercise = exercise
        # self.result = None
        self.acc = 0
        self.loss = 0.0

    def run(self):
        acc, loss = self.classify.TrainEMG()
        self.taskFinished.emit()
        self.acc = acc
        self.loss = loss
