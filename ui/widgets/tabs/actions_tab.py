from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from helpers.classification import Classification
from ui.widgets.custom_styles import QStyles
from ui.widgets.dialogs.calibrate_dialog import CalibrateDialog
from ui.widgets.dialogs.session_dialog import SessionDialog


class ActionsTab(QWidget):
    def __init__(self, parent=None,
                 classification: Classification = None,
                 patient=None):
        super(ActionsTab, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.classification = classification
        self.patient = patient
        self.initUi()

    def initUi(self):
        sessionButton = QPushButton("Session")
        sessionButton.setStyleSheet(QStyles.styledButtonStyle)
        sessionButton.clicked.connect(self.onSessionClicked)
        sessionButton.setFixedSize(120, 30)

        widget = QWidget()
        actionButtons = QVBoxLayout()
        widget.setLayout(actionButtons)
        calibrateButton = QPushButton("Calibrate")
        calibrateButton.setStyleSheet(QStyles.styledButtonStyle)
        calibrateButton.clicked.connect(self.onCalibrateClicked)
        calibrateButton.setFixedSize(120, 30)

        label = QLabel("or")
        actionButtons.addWidget(sessionButton)
        actionButtons.addWidget(label)
        actionButtons.addWidget(calibrateButton)
        actionButtons.setAlignment(sessionButton, Qt.Alignment.AlignCenter)
        actionButtons.setAlignment(label, Qt.Alignment.AlignCenter)
        actionButtons.setAlignment(calibrateButton, Qt.Alignment.AlignCenter)

        self.layout().addWidget(widget)

    def onSessionClicked(self):
        print("Session clicked")
        dialog = SessionDialog(self)
        dialog.exec()

    def onCalibrateClicked(self):
        print("Calibrating model")
        print(self.patient)
        if self.patient is not None:
            dialog = CalibrateDialog(
                classification=self.classification,
                patient=self.patient)
            dialog.exec()
