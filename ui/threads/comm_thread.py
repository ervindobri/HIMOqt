import time

from PyQt6 import QtCore
from PyQt6.QtCore import QThread

from helpers.classification import Classification
from helpers.communication import LocalCommunication


class CommThread(QThread):
    currentExercise = QtCore.pyqtSignal()
    replySignal = QtCore.pyqtSignal(int)

    def __init__(self,
                 communication : LocalCommunication = None,
                 classify: Classification = None,
                 ):
        QThread.__init__(self)
        self.classify = classify
        self.communication = communication

    def run(self):
        self.communication.start_listen()
        while True:
            self.replySignal.emit(self.classify.current_exercise)
            res, reply = self.communication.listen(self.classify.current_exercise)
            if not res:
                break

    def stop(self):
        # self.communication.stop_listen()
        self.terminate()
