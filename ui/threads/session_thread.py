from PyQt6 import QtCore
from PyQt6.QtCore import QThread


class SessionThread(QThread):
    exerciseResult = QtCore.pyqtSignal(str)

    def __init__(self, classification, parent=None):
        QThread.__init__(self, parent)
        # self.queue = queue
        # self.result_queue = result_queue
        self.classification = classification

    def run(self):
        self.classification.LoadModel()
        while True:
            res = self.classification.Predict()
            self.exerciseResult.emit(res)


def handle_results(result_queue):
    while True:
        result = result_queue.get()
        print("Got result {}".format(result))
