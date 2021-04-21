from PyQt6 import QtWidgets


class QHSeparationLine(QtWidgets.QFrame):
    '''
  a horizontal seperation line\n
  '''

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(2)
        self.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        self.setStyleSheet("QFrame {background-color: #cccccc;}")
        return


class QVSeparationLine(QtWidgets.QFrame):
    '''
  a vertical seperation line\n
  '''

    def __init__(self):
        super().__init__()
        self.setFixedWidth(20)
        self.setMinimumHeight(1)
        self.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        return
