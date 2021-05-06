from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QPushButton, QComboBox, QLabel, QHBoxLayout, \
    QTimeEdit

from helpers.constants import PREDEFINED_PARAMETERS, RESOURCES_PATH, STANDING
from models.session import Session
from ui.threads.session_thread import SessionThread
from ui.widgets.custom.custom_styles import QStyles


class IntegratedSessionDialog(QDialog):
    def __init__(self, classification, parent=None):
        super().__init__(parent)

        self.currentExerciseLabel = QLabel('None')
        self.startButton = QPushButton('Start Session')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.window().setFixedSize(200, 200)
        self.setWindowTitle('Game Session')
        self.initUi()

        self.currentExercise = ""
        self.sessionThread = SessionThread(classification)
        self.sessionThread.exerciseResult.connect(self.onResultExercise)

    def onResultExercise(self, value):
        self.currentExerciseLabel.setText(value)

    def initUi(self):
        font = self.currentExerciseLabel.font()
        font.setPointSize(15)
        self.currentExerciseLabel.setFont(font)
        self.startButton.setStyleSheet(QStyles.styledButtonStyle)
        self.startButton.clicked.connect(self.startGameSession)
        self.startButton.setFixedHeight(35)
        self.layout.addWidget(self.currentExerciseLabel)
        self.layout.addWidget(self.startButton)

        self.layout.setAlignment(self.currentExerciseLabel, Qt.Alignment.AlignCenter)
        # todo
        pass

    def startGameSession(self):
        if not self.sessionThread.isRunning():
            self.sessionThread.start()
            self.startButton.setText("Stop Session")
            self.startButton.setStyleSheet(QStyles.outlineButtonStyle)
        else:
            self.sessionThread.terminate()
            self.startButton.setText("Start Session")
            self.startButton.setStyleSheet(QStyles.styledButtonStyle)
