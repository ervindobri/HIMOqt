from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from helpers.classification import Classification
from ui.widgets.custom.custom_styles import QStyles
from ui.widgets.dialogs.calibrate_dialog import CalibrateDialog
from ui.widgets.dialogs.integrated_session_dialog import IntegratedSessionDialog
from ui.widgets.dialogs.session_dialog import SessionDialog


class ActionsTab(QWidget):
    def __init__(self, parent=None,
                 classification: Classification = None,
                 communication=None,
                 patient=None):
        super(ActionsTab, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.classification = classification
        self.communication = communication
        self.patient = patient
        self.initUi()


    def initUi(self):
        sessionButton = QPushButton("Standalone Session")
        font = sessionButton.font()
        font.setPointSize(15)

        sessionButton.setStyleSheet(QStyles.styledButtonStyle)
        sessionButton.clicked.connect(self.onSessionClicked)
        sessionButton.setFixedSize(200, 40)
        sessionButton.setFont(font)

        gameSessionButton = QPushButton("Game Session")
        gameSessionButton.setStyleSheet(QStyles.styledButtonStyle)
        gameSessionButton.clicked.connect(self.onGameSessionClicked)
        gameSessionButton.setFixedSize(200, 40)
        gameSessionButton.setFont(font)

        widget = QWidget()
        actionButtons = QVBoxLayout()
        widget.setLayout(actionButtons)
        calibrateButton = QPushButton("Calibrate")
        calibrateButton.setStyleSheet(QStyles.outlineButtonStyle)
        calibrateButton.clicked.connect(self.onCalibrateClicked)
        calibrateButton.setFixedSize(200, 40)
        calibrateButton.setFont(font)

        label = QLabel("or")
        actionButtons.addWidget(sessionButton)
        actionButtons.addWidget(gameSessionButton)
        actionButtons.addWidget(label)
        actionButtons.addWidget(calibrateButton)
        actionButtons.setAlignment(sessionButton, Qt.AlignmentFlag.AlignCenter)
        actionButtons.setAlignment(gameSessionButton, Qt.AlignmentFlag.AlignCenter)
        actionButtons.setAlignment(label, Qt.AlignmentFlag.AlignCenter)
        actionButtons.setAlignment(calibrateButton, Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(widget)

    def onGameSessionClicked(self):
        print("Game session")

        if self.patient is not None:
            dialog = IntegratedSessionDialog(
                classification=self.classification,
                communication=self.communication
            )
            dialog.exec()

    def onSessionClicked(self):
        print("Session clicked")
        if self.patient is not None:
            dialog = SessionDialog(self.classification)
            dialog.exec()

    def onCalibrateClicked(self):
        print("Calibrating model")
        print(self.patient)
        if self.patient is not None:
            dialog = CalibrateDialog(
                classification=self.classification,
                patient=self.patient)
            dialog.exec()
