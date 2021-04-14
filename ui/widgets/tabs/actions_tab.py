from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from ui.widgets.calibrate_dialog import CalibrateDialog
from ui.widgets.custom_styles import QStyles
from ui.widgets.session_dialog import SessionDialog


class ActionsTab(QWidget):
    def __init__(self, parent, classification):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.classification = classification
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
        actionButtons.setAlignment(sessionButton, Qt.AlignCenter)
        actionButtons.setAlignment(label, Qt.AlignCenter)
        actionButtons.setAlignment(calibrateButton, Qt.AlignCenter)

        self.layout().addWidget(widget)

    def onSessionClicked(self):
        print("Session clicked")
        dialog = SessionDialog(self)
        dialog.exec_()

    def onCalibrateClicked(self):
        print("Calibrating model")
        dialog = CalibrateDialog(self, self.classification)
        dialog.exec_()