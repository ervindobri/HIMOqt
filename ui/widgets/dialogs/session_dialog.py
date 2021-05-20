from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QPushButton, QComboBox, QLabel, QHBoxLayout, \
    QTimeEdit

from helpers.constants import PREDEFINED_PARAMETERS, RESOURCES_PATH, STANDING
from models.session import Session
from ui.threads.session_thread import SessionThread
from ui.widgets.custom.custom_styles import QStyles


class SessionDialog(QDialog):
    def __init__(self, classification, parent=None):
        super().__init__(parent)
        self.window().setWindowTitle('Standalone Session')
        self.image = QLabel()
        self.freestyleTimer = QTimer()
        self.freestyleTime = QTime(0, 5, 0)
        self.freestyleTimeEdit = QTimeEdit(self.freestyleTime)
        self.repsInput = QComboBox()
        self.nextExerciseName = QLabel('Next: Pause')
        self.currentExerciseCount = QLabel('0/15')
        self.currentExerciseLabel = QLabel('Exercise name')
        self.pause = QLabel('10')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.window().setFixedSize(800, 500)
        self.tabLayout = QTabWidget()
        self.parametersTab = QWidget()
        self.exercisesTab = QWidget()
        self.freestyleTab = QWidget()
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
        self.tabLayout.setStyleSheet(QStyles.tabStyle)
        self.setParametersTab()
        self.setExercisesTab()

    def setParametersTab(self):
        layout = QVBoxLayout()
        self.parametersTab.setLayout(layout)
        container = QWidget()
        layout.addWidget(container)
        containerLayout = QVBoxLayout()
        container.setLayout(containerLayout)
        layout.setAlignment(container, Qt.AlignmentFlag.AlignCenter)

        startButton = QPushButton('Start')
        font = startButton.font()
        font.setPointSize(13)

        startButton.clicked.connect(self.startSession)
        startButton.setStyleSheet(QStyles.styledButtonStyle)
        startButton.setFixedSize(200, 35)
        startButton.setFont(font)
        startButton.setContentsMargins(10, 30, 10, 10)

        label1 = QLabel('Exercises will repeat this many times:')
        label1.setFont(font)
        label1.setStyleSheet(QStyles.labelStyle)
        self.repsInput.addItems(PREDEFINED_PARAMETERS)
        self.repsInput.setStyleSheet(QStyles.comboStyle)
        self.repsInput.setFixedSize(200, 35)
        self.repsInput.currentTextChanged.connect(self.onRepsChanged)
        self.repsInput.setFont(font)
        self.repsInput.setContentsMargins(10, 10, 10, 30)

        label2 = QLabel('Pause between exercises(second):')
        label2.setFont(font)
        label2.setStyleSheet(QStyles.labelStyle)

        self.pause.setStyleSheet("border: 1px solid #20c1dc; border-radius: 7px;")
        self.pause.setFixedSize(200, 35)
        self.pause.setFont(font)
        self.pause.setContentsMargins(10, 10, 10, 30)
        self.pause_time = self.pause.text()
        containerLayout.addWidget(label1)
        containerLayout.addWidget(self.repsInput)
        containerLayout.addWidget(label2)
        containerLayout.addWidget(self.pause)
        containerLayout.addWidget(startButton)
        containerLayout.setAlignment(self.repsInput, Qt.AlignmentFlag.AlignCenter)
        containerLayout.setStretch(0, 1)
        containerLayout.setStretch(1, 2)
        containerLayout.setAlignment(self.pause, Qt.AlignmentFlag.AlignCenter)
        containerLayout.setAlignment(startButton, Qt.AlignmentFlag.AlignCenter)

    def onRepsChanged(self, text):
        self.reps = text
        pause = int(text) * 2
        self.pause.setText(str(pause))
        self.pause_time = pause
        self.pause_time_left = self.pause_time

    def startSession(self):
        self.reps = self.repsInput.currentText()
        self.pause_time = int(self.pause.text())
        print("reps:", self.reps)

        # Set session properties
        self.session = Session(
            reps=self.reps,
            pause=self.pause.text()
        )
        # get the label for first exercise
        self.currentExerciseCount.setText(self.session.current_status())
        self.nextExerciseName.setText("Next: Pause " + str(self.session.pause) + "secs")
        # Start therapy
        self.tabLayout.setCurrentIndex(1)
        if not self.sessionThread.isRunning():
            self.sessionThread.start()

    def setExercisesTab(self):
        layout = QVBoxLayout()
        self.exercisesTab.setLayout(layout)
        font = self.image.font()
        font.setPointSize(13)
        bigFont = font
        bigFont.setPointSize(17)

        self.image.setPixmap(QPixmap(RESOURCES_PATH + 'frame.png'))
        self.image.setFixedHeight(100)
        container = QVBoxLayout()
        self.currentExerciseLabel.setFont(font)
        self.currentExerciseCount.setFont(bigFont)
        self.currentExerciseCount.setStyleSheet(
            "background-color: #20c1dc; border-radius: 7px; color: white; padding: 5px;")
        self.currentExerciseCount.setContentsMargins(10, 10, 10, 10)

        clabel = QLabel('Current exercise')
        nlabel = QLabel('Next exercise')
        clabel.setFont(font)
        nlabel.setFont(font)

        exerciseContainer = QHBoxLayout()
        nextContainer = QVBoxLayout()
        nextContainer.addWidget(nlabel)
        nextContainer.addWidget(self.nextExerciseName)
        nextContainer.setAlignment(nlabel, Qt.AlignmentFlag.AlignTop)
        nextContainer.setAlignment(self.nextExerciseName, Qt.AlignmentFlag.AlignTop)

        container.addWidget(clabel)
        container.addWidget(self.currentExerciseCount)
        container.addWidget(self.image)
        container.addWidget(self.currentExerciseLabel)
        container.addWidget(self.nextExerciseName)
        container.setAlignment(clabel, Qt.AlignmentFlag.AlignCenter)
        container.setAlignment(self.currentExerciseCount, Qt.AlignmentFlag.AlignCenter)
        container.setAlignment(self.image, Qt.AlignmentFlag.AlignCenter)
        container.setAlignment(self.currentExerciseLabel, Qt.AlignmentFlag.AlignCenter)
        container.setAlignment(self.nextExerciseName, Qt.AlignmentFlag.AlignCenter)
        exerciseContainer.addLayout(container, stretch=2)
        # exerciseContainer.addLayout(nextContainer, stretch=1)
        layout.addLayout(exerciseContainer)

        stopButton = QPushButton('Stop')
        stopButton.setStyleSheet(QStyles.outlineButtonStyle)
        stopButton.setFixedSize(120, 35)
        stopButton.clicked.connect(self.onSessionStopped)
        layout.addWidget(stopButton)

        layout.setAlignment(container, Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(stopButton, Qt.AlignmentFlag.AlignRight)

    def startFreestyle(self):
        # Set connection
        self.sessionThread.exerciseResult.disconnect()
        self.sessionThread.exerciseResult.connect(self.onResultFreestyle)
        # Start timer
        self.freestyleTimeEdit.setDisplayFormat("hh:mm:ss")
        self.freestyleTimer.timeout.connect(self.freestyle_timeout)
        self.freestyleTimer.start(1000)
        self.currentExerciseCount.setText(self.freestyleTimeEdit.text())
        # Set texts:
        self.currentExerciseLabel.setText("Freestyle")
        self.nextExerciseName.setText("Next: All completed.")
        pass

    def onResultExercise(self, value):
        self.currentExerciseLabel.setText(self.session.current_exercise_name)
        result = self.session.increment(value)
        if not self.session.pause_active:
            if result:
                self.image.setPixmap(QPixmap(RESOURCES_PATH + 'success.png'))
            else:
                # print("Not correct.")
                self.image.setPixmap(QPixmap(RESOURCES_PATH + 'frame.png'))

            # If standing on toes: start timer
            if self.session.current_exercise_name == STANDING:
                if not self.pauseTimer.isActive():
                    self.nextExerciseName.setText("Next: Freestyle - 5min")

                    self.pause_time_left = self.pause_time * 2
                    self.pauseTimer.start(1000)
            else:
                self.currentExerciseCount.setText(self.session.current_status())
                self.nextExerciseName.setText("Next: Pause " + str(self.session.pause) + "secs")

        else:
            # TODO: set timer and start, after pause time -> set flag
            self.currentExerciseLabel.setText("Pause")
            self.nextExerciseName.setText("Next: " + self.session.next_exercise_name)
            if not self.pauseTimer.isActive():
                self.session.done += 1
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
                self.startFreestyle()
                self.pauseTimer.stop()
            pass

    def onResultFreestyle(self, value):
        self.currentExerciseLabel.setText(value)

    def freestyle_timeout(self):
        self.freestyleTimeEdit.setTime(self.freestyleTimeEdit.time().addSecs(-1))
        if self.freestyleTimeEdit.time() > QTime(0, 0, 0):

            curr = self.freestyleTimeEdit.time()
            self.currentExerciseCount.setText(curr.toString("hh:mm:ss"))
        else:
            # stop session and timer
            self.freestyleTimer.stop()
            self.onSessionStopped()
        pass

    def onSessionStopped(self):
        self.sessionThread.terminate()
        self.freestyleTimer.stop()
        self.pauseTimer.stop()
        print("Session thread stopped!")
        self.currentExerciseLabel.setText("Finished")
