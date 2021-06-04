from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel

from ui.threads.comm_thread import CommThread
from ui.threads.session_thread import SessionThread
from ui.widgets.custom.custom_styles import QStyles
from ui.widgets.dialogs.show_dialog import CustomDialog


class IntegratedSessionDialog(QDialog):
    def __init__(self,
                 classification=None,
                 communication=None,
                 parent=None):
        super().__init__(parent)

        self.currentExerciseLabel = QLabel('None')
        self.currentCodePipe = QLabel('Sent: 0')
        self.startButton = QPushButton('Start Session')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.window().setFixedSize(200, 200)
        self.setWindowTitle('Game Session')
        self.initUi()

        self.currentExercise = ""
        self.sessionThread = SessionThread(classification)
        self.sessionThread.exerciseResult.connect(self.onResultExercise)
        self.sessionThread.exists.connect(self.modelExists)
        self.sessionThread.holding = True
        self.communicationThread = CommThread(
            communication,
            classification
        )
        self.communicationThread.replySignal.connect(self.onPipeReply)

    def onPipeReply(self, value):
            self.currentCodePipe.setText("Sent: " + str(value))

    # Show messagebox if model does not exist -> go to calibrate
    def modelExists(self, value):
        if not value:
            print("Not exists!")
            CustomDialog.warningMessage(
                text="No model for patient",
                info="You need to calibrate the patient in order to do a session.")

    def onResultExercise(self, value):
        self.currentExerciseLabel.setText(value)

    def initUi(self):
        font = self.currentExerciseLabel.font()
        font.setPointSize(15)
        self.currentExerciseLabel.setFont(font)
        self.startButton.setStyleSheet(QStyles.styledButtonStyle)
        self.startButton.clicked.connect(self.startGameSession)
        self.startButton.setFixedHeight(35)
        self.startButton.setFont(font)
        self.layout.addWidget(self.currentExerciseLabel)
        self.layout.addWidget(self.currentCodePipe)
        self.layout.addWidget(self.startButton)

        self.layout.setAlignment(self.currentExerciseLabel, Qt.AlignmentFlag.AlignCenter)
        self.layout.setAlignment(self.currentCodePipe, Qt.AlignmentFlag.AlignBottom)
        # todo
        pass

    def startGameSession(self):
        try:
            print(self.sessionThread.isRunning())
            if not self.sessionThread.isRunning():
                self.communicationThread.start()
                self.sessionThread.start()
                self.startButton.setText("Stop Session")
                self.startButton.setStyleSheet(QStyles.outlineButtonStyle)
            else:
                self.sessionThread.terminate()
                self.communicationThread.stop()
                self.startButton.setText("Start Session")
                self.startButton.setStyleSheet(QStyles.styledButtonStyle)
        except Exception as e:
            print(e)

    def reject(self):
        if self.sessionThread.isRunning():
            self.sessionThread.terminate()
            self.communicationThread.stop()
            self.startButton.setText("Start Session")
            self.startButton.setStyleSheet(QStyles.styledButtonStyle)
            super().reject()
