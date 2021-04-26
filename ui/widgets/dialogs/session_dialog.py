import queue
import threading

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QPushButton, QComboBox, QLabel, QHBoxLayout

from helpers.constants import PREDEFINED_PARAMETERS, RESOURCES_PATH
from models.session import Session
from ui.threads.session_thread import SessionThread
from ui.widgets.custom_styles import QStyles


class SessionDialog(QDialog):
    def __init__(self, classification, parent=None):
        super().__init__(parent)
        self.repsInput = QComboBox()
        self.nextExerciseName = QLabel('blabla')
        self.currentExerciseCount = QLabel('0/15')
        self.currentExerciseLabel = QLabel('Exercise name')
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

        self.reps = None
        self.session = None
        self.pauseTimer = QTimer()
        self.pauseTimer.timeout.connect(self.timer_timeout)
        self.pause_time = 0
        self.pause_time_left = self.pause_time

        self.sessionThread = SessionThread(classification)
        self.sessionThread.exerciseResult.connect(self.onResultExercise)

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
        self.repsInput.addItems(PREDEFINED_PARAMETERS)
        self.repsInput.setStyleSheet(QStyles.comboStyle)
        self.repsInput.setFixedSize(200, 35)
        self.repsInput.currentTextChanged.connect(self.onRepsChanged)
        self.repsInput.setFont(font)

        label2 = QLabel('With pauses of (second):')
        label2.setStyleSheet(QStyles.labelStyle)

        self.pause.setStyleSheet(QStyles.comboStyle)
        self.pause.setFixedSize(200, 35)
        self.pause.setFont(font)

        containerLayout.addWidget(label1)
        containerLayout.addWidget(self.repsInput)
        containerLayout.addWidget(label2)
        containerLayout.addWidget(self.pause)
        containerLayout.addWidget(startButton)
        containerLayout.setAlignment(startButton, Qt.Alignment.AlignCenter)

    def onRepsChanged(self, text):
        self.reps = text
        pause = int(text) * 2
        self.pause.setText(str(pause))
        self.pause_time = pause
        self.pause_time_left = self.pause_time

    def startSession(self):
        self.reps = self.repsInput.currentText()
        print("reps:", self.reps)

        # Set session properties
        self.session = Session(
            reps=self.reps,
            pause=self.pause.text()
        )
        # get the label for first exercise
        self.currentExerciseCount.setText(self.session.current_status())
        # Start therapy
        self.tabLayout.setCurrentIndex(1)
        if not self.sessionThread.isRunning():
            self.sessionThread.start()

    def setExercisesTab(self):
        layout = QVBoxLayout()
        self.exercisesTab.setLayout(layout)
        self.image = QLabel()
        font = self.image.font()
        font.setPointSize(13)
        self.image.setPixmap(QPixmap(RESOURCES_PATH + 'frame.png'))
        self.image.setFixedHeight(100)
        container = QVBoxLayout()
        self.currentExerciseLabel.setFont(font)
        self.currentExerciseCount.setFont(font)
        clabel = QLabel('Current exercise')
        nlabel = QLabel('Next exercise')
        clabel.setFont(font)
        nlabel.setFont(font)

        exerciseContainer = QHBoxLayout()
        nextContainer = QVBoxLayout()
        nextContainer.addWidget(nlabel)
        nextContainer.addWidget(self.nextExerciseName)
        nextContainer.setAlignment(nlabel, Qt.Alignment.AlignTop)
        nextContainer.setAlignment(self.nextExerciseName, Qt.Alignment.AlignTop)

        container.addWidget(clabel)
        container.addWidget(self.currentExerciseCount)
        container.addWidget(self.image)
        container.addWidget(self.currentExerciseLabel)
        container.setAlignment(clabel, Qt.Alignment.AlignCenter)
        container.setAlignment(self.currentExerciseCount, Qt.Alignment.AlignCenter)
        container.setAlignment(self.image, Qt.Alignment.AlignCenter)
        container.setAlignment(self.currentExerciseLabel, Qt.Alignment.AlignCenter)
        exerciseContainer.addLayout(container, stretch=2)
        exerciseContainer.addLayout(nextContainer, stretch=1)
        layout.addLayout(exerciseContainer)

        stopButton = QPushButton('Stop')
        stopButton.setStyleSheet(QStyles.outlineButtonStyle)
        stopButton.setFixedSize(120, 35)
        stopButton.clicked.connect(self.onSessionStopped)
        layout.addWidget(stopButton)

        layout.setAlignment(container, Qt.Alignment.AlignCenter)
        layout.setAlignment(stopButton, Qt.Alignment.AlignRight)

    def onResultExercise(self, value):
        self.currentExerciseLabel.setText(self.session.current_exercise_name)
        result = self.session.increment(value)
        if not self.session.pause_active:
            if result:
                # print("Correct!")
                self.image.setPixmap(QPixmap(RESOURCES_PATH + 'success.png'))

            else:
                # print("Not correct.")
                self.image.setPixmap(QPixmap(RESOURCES_PATH + 'frame.png'))

            # If standing on toes: start timer
            if self.session.current_exercise_name == "Stand on your toes":
                self.nextExerciseName.setText("")
                if not self.pauseTimer.isActive():
                    print("Standing on your toes!")
                    self.pause_time_left = self.pause_time * 2
                    self.pauseTimer.start(1000)
            else:
                self.currentExerciseCount.setText(self.session.current_status())

        else:
            # TODO: set timer and start, after pause time -> set flag
            self.currentExerciseLabel.setText("Pause")
            if self.session.session_finished:
                self.currentExerciseLabel.setText("Finished")

            if not self.pauseTimer.isActive():
                self.session.done += 1
                print("Pause!")
                self.pause_time_left = self.pause_time
                self.pauseTimer.start(1000)

    def timer_timeout(self):
        self.pause_time_left -= 1
        self.currentExerciseCount.setText(str(self.pause_time_left))
        self.session.standing_on_toes_secs += 1
        if self.pause_time_left == 0:
            print("Time left!")
            self.pauseTimer.stop()
            self.session.pause_active = False

            if self.session.session_finished:
                self.onSessionStopped()
            pass

    def onSessionStopped(self):
        self.sessionThread.terminate()
        print("Session thread stopped!")

    def setResultsTab(self):
        pass
