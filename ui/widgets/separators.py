from PyQt5 import QtWidgets


class QHSeparationLine(QtWidgets.QFrame):
    '''
  a horizontal seperation line\n
  '''

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(2)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
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
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        return
