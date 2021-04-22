import queue
import threading

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QPushButton, QComboBox, QLabel

from helpers.constants import PREDEFINED_PARAMETERS, RESOURCES_PATH
from ui.threads.session_thread import handle_results, SessionThread
from ui.widgets.custom_styles import QStyles


class SessionDialog(QDialog):
    def __init__(self, classification, parent=None):
        super().__init__(parent)
        self.currentExerciselabel = QLabel('Exercise name')
        self.pause = QLabel('30')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.window().setFixedSize(800, 500)
        self.tabLayout = QTabWidget()
        self.parametersTab = QWidget()
        self.exercisesTab = QWidget()
        self.resultsTab = QWidget()

        self.layout.addWidget(self.tabLayout)
        self.initUi()

        self.sessionThread = SessionThread(classification)
        self.sessionThread.exerciseResult.connect(self.onResultExercise)

    def onResultExercise(self, value):
        self.currentExerciselabel.setText(value)

    def initUi(self):
        self.tabLayout.addTab(self.parametersTab, "Parameters")
        self.tabLayout.addTab(self.exercisesTab, "Exercises")
        self.tabLayout.addTab(self.resultsTab, "Results")
        self.tabLayout.setStyleSheet(QStyles.tabStyle)

        self.setParametersTab()
        self.setExercisesTab()
        self.setResultsTab()

    def setParametersTab(self):
        layout = QVBoxLayout()
        self.parametersTab.setLayout(layout)
        container = QWidget()
        layout.addWidget(container)
        containerLayout = QVBoxLayout()
        container.setLayout(containerLayout)
        container.setFixedWidth(300)
        layout.setAlignment(container, Qt.Alignment.AlignCenter)

        startButton = QPushButton('Start')
        font = startButton.font()
        font.setPointSize(13)

        startButton.clicked.connect(self.startSession)
        startButton.setStyleSheet(QStyles.styledButtonStyle)
        startButton.setFixedSize(120, 35)

        label1 = QLabel('Exercises will repeat this many times:')
        label1.setStyleSheet(QStyles.labelStyle)
        repsInput = QComboBox()
        repsInput.addItems(PREDEFINED_PARAMETERS)
        repsInput.setStyleSheet(QStyles.comboStyle)
        repsInput.setFixedSize(200, 35)
        repsInput.currentTextChanged.connect(self.onRepsChanged)
        repsInput.setFont(font)

        label2 = QLabel('With pauses of (second):')
        label2.setStyleSheet(QStyles.labelStyle)

        self.pause.setStyleSheet(QStyles.comboStyle)
        self.pause.setFixedSize(200, 35)
        self.pause.setFont(font)

        containerLayout.addWidget(label1)
        containerLayout.addWidget(repsInput)
        containerLayout.addWidget(label2)
        containerLayout.addWidget(self.pause)
        containerLayout.addWidget(startButton)
        containerLayout.setAlignment(startButton, Qt.Alignment.AlignCenter)

    def onRepsChanged(self, text):
        self.pause.setText(str(int(text)*2))

    def startSession(self):
        self.tabLayout.setCurrentIndex(1)
        self.queue = queue.Queue()
        self.result_queue = queue.Queue()

        # result_handler = threading.Thread(target=handle_results, self.result_queue)
        self.sessionThread.start()

    def setExercisesTab(self):
        layout = QVBoxLayout()
        self.exercisesTab.setLayout(layout)
        image = QLabel()
        font = image.font()
        font.setPointSize(13)
        image.setPixmap(QPixmap(RESOURCES_PATH + 'frame.png'))
        image.setFixedHeight(100)
        container = QVBoxLayout()
        self.currentExerciselabel.setFont(font)
        container.addWidget(image)
        container.addWidget(self.currentExerciselabel)
        container.setAlignment(image, Qt.Alignment.AlignCenter)
        container.setAlignment(self.currentExerciselabel, Qt.Alignment.AlignCenter)
        layout.addLayout(container)

        stopButton = QPushButton('Stop')
        stopButton.setStyleSheet(QStyles.outlineButtonStyle)
        stopButton.setFixedSize(120, 35)
        stopButton.clicked.connect(self.onSessionStopped)
        layout.addWidget(stopButton)

        layout.setAlignment(container, Qt.Alignment.AlignCenter)
        layout.setAlignment(stopButton, Qt.Alignment.AlignRight)
        pass

    def onSessionStopped(self):
        self.sessionThread.exit()
        print("Session thread stopped!")

    def setResultsTab(self):
        pass