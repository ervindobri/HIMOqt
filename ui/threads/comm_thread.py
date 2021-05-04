import time

from PyQt6 import QtCore
from PyQt6.QtCore import QThread

from helpers.classification import Classification
from helpers.communication import SocketCommunication


class CommThread(QThread):
    currentExercise = QtCore.pyqtSignal()
    replySignal = QtCore.pyqtSignal(str)

    def __init__(self,
                 communication : SocketCommunication = None,
                 classify: Classification = None,
                 ):
        QThread.__init__(self)
        self.classify = classify
        self.communication = communication

    def run(self):
        while True:
            res, reply = self.communication.listen(self.classify.current_exercise)
            if not res:
                break
            self.replySignal.emit(reply)
            time.sleep(1)
