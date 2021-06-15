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
        self.setFixedWidth(450)
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
        warning = QLabel('THE FOLLOWING ACTIONS REQUIRE AN ALREADY SELECTED AND CALIBRATED PATIENT.')
        warning.setWordWrap(True)
        warning.setFixedHeight(50)
        warning.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(warning)
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
                       "you must create his/her calibration data "
                       "by clicking the 'Calibrate' button on the 'Actions' tab. "
                       )
        label.setWordWrap(True)
        label1 = QLabel("1. Press 'Record' for each exercise/movement. Recording takes 2sec/exercise. "
                        "Record next after previous is successful.")
        label1.setWordWrap(True)
        label2 = QLabel("2. Make sure all three have a check mark (meaning recording was successful).")
        label3 = QLabel("3. Press 'Train' to train the model. Accuracy should be 100% for better recognition.")
        label4 = QLabel("4. Press 'Ready' to close dialog and begin session.")
        self.calibrateLayout.addWidget(warning)
        self.calibrateLayout.addWidget(label)
        self.calibrateLayout.addWidget(label1)
        self.calibrateLayout.addWidget(label2)
        self.calibrateLayout.addWidget(label3)
        self.calibrateLayout.addWidget(label4)

    def createSessionLayout(self):
        title = QLabel("Standalone Session")
        font = title.font()
        font.setBold(True)
        title.setFont(font)
        self.sessionLayout.addWidget(title)
        label = QLabel('Fixed exercise session consisting of 3'
                       ' foot exercises: raising on toes, toe clenching and standing on toes.'
                       ' It is followed by a 5 minute session of freestyle - practice any of the exercises.')
        label.setWordWrap(True)
        label2 = QLabel("1. Select parameters (repetitions) and start session.")
        label3 = QLabel("2. Follow exercises according to the instructions.")
        label4 = QLabel("3. Finish session, exit screen.")
        self.sessionLayout.addWidget(label)
        self.sessionLayout.addWidget(label2)
        self.sessionLayout.addWidget(label3)
        self.sessionLayout.addWidget(label4)

    def createGameLayout(self):
        title = QLabel("Game Session")
        font = title.font()
        font.setBold(True)
        title.setFont(font)
        self.gameLayout.addWidget(title)
        label = QLabel("The software can be used with a game. The game needs to be OPENED and ready."
                       )
        label2 = QLabel("1. On the 'Server' tab press Connect to connect to the game. "
                        "Default port is entered, can be modified.")
        label3 = QLabel("2. Press 'Game Session' on the 'Actions' tab and 'Start session' "
                        "on the dialog to practice foot exercises.")
        label4 = QLabel("3. Stop session after finishing therapy.")
        label.setWordWrap(True)
        self.gameLayout.addWidget(label)
        self.gameLayout.addWidget(label2)
        self.gameLayout.addWidget(label3)
        self.gameLayout.addWidget(label4)

    def onAcceptClicked(self):
        print("Accept")
        self.close()
