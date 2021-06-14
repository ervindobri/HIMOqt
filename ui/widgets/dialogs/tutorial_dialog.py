import functools
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from models.patient import Patient
from ui.widgets.custom.custom_styles import QStyles


class TutorialDialog(QDialog):
    def __init__(self, parent,
                 ):
        super(TutorialDialog, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.setWindowTitle("How to use this app?")
        self.setFixedSize(400, 500)
        self.setLayout(layout)

        self.acceptButton = QPushButton('Accept')
        self.acceptButton.clicked.connect(self.onAcceptClicked)
        self.acceptButton.setStyleSheet(QStyles.styledButtonStyle)
        self.acceptButton.setFixedSize(100, 35)

        self.calibrateLayout = QVBoxLayout()
        self.sessionLayout = QVBoxLayout()
        self.gameLayout = QVBoxLayout()
        self.createCalibrationLayout()
        self.createSessionLayout()
        self.createGameLayout()

        layout.addLayout(self.calibrateLayout)
        layout.addLayout(self.sessionLayout)
        layout.addLayout(self.gameLayout)
        layout.addWidget(self.acceptButton)
        layout.setAlignment(self.acceptButton, Qt.AlignmentFlag.AlignHCenter)

    def createCalibrationLayout(self):
        title = QLabel("Calibration")
        font = title.font()
        font.setBold(True)
        title.setFont(font)
        self.calibrateLayout.addWidget(title)
        warning = QLabel('IT IS SUGGESTED TO RECALIBRATE BEFORE EVERY SESSION.')
        warning.setStyleSheet("color: red; font-weight: bold;")

        label = QLabel("After selecting a patient (from the list), "
                       "you should be able to create his/her calibration data "
                       "by clicking the Calibrate button. "
                       "After recording data for all three movements, "
                       "the software will create a personalized model which can be used in the session."
                       )
        label.setWordWrap(True)
        self.calibrateLayout.addWidget(warning)
        self.calibrateLayout.addWidget(label)

    def createSessionLayout(self):
        title = QLabel("Standalone Session")
        font = title.font()
        font.setBold(True)
        title.setFont(font)
        self.calibrateLayout.addWidget(title)
        label = QLabel('Fixed exercise session consisting of 3'
                       ' foot exercises: raising on toes, toe clenching and standing on toes.'
                       ' It is followed by a 5 minute session of freestyle - practice any of the exercises.')
        label.setWordWrap(True)
        label1 = QLabel("1. Select patient and calibrate him/her.")
        label2 = QLabel("2. Select parameters (repetitions) and start session.")
        label3 = QLabel("3. Follow exercises according to the instructions.")
        label4 = QLabel("4. Finish session, exit screen.")
        self.calibrateLayout.addWidget(label)
        self.calibrateLayout.addWidget(label1)
        self.calibrateLayout.addWidget(label2)
        self.calibrateLayout.addWidget(label3)
        self.calibrateLayout.addWidget(label4)

    def createGameLayout(self):
        title = QLabel("Game Session")
        font = title.font()
        font.setBold(True)
        title.setFont(font)
        self.calibrateLayout.addWidget(title)
        label = QLabel("The software can be used with a game. The game needs to be OPENED and ready."
                       )
        label1 = QLabel("1. Select patient and calibrate him/her.")
        label2 = QLabel("2. On the 'Server' tab press Connect to connect to the game.")
        label3 = QLabel("3. Press 'Game Session' on the 'Actions' tab to practice foot exercises.")
        label4 = QLabel("4. Stop session after finishing therapy.")
        label.setWordWrap(True)
        self.calibrateLayout.addWidget(label)
        self.calibrateLayout.addWidget(label1)
        self.calibrateLayout.addWidget(label2)
        self.calibrateLayout.addWidget(label3)
        self.calibrateLayout.addWidget(label4)

    def onAcceptClicked(self):
        print("Accept")
        self.close()
