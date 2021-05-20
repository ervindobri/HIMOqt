import functools

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QProgressBar
from PyQt6.QtGui import QPixmap

from helpers.classification import Classification
from helpers.constants import RESOURCES_PATH
from models.patient import Patient
from ui.widgets.dialogs.show_dialog import CustomDialog
from ui.threads.record_thread import RecordThread
from ui.threads.train_thread import TrainThread
from ui.widgets.custom.custom_styles import QStyles


class CalibrateDialog(QDialog):
    def __init__(self, parent=None,
                 classification: Classification = None,
                 patient: Patient = None
                 ):
        super(CalibrateDialog, self).__init__(parent)
        self.classification = classification
        self.patient = patient

        layout = QVBoxLayout()
        self.setFixedSize(700, 500)
        self.setLayout(layout)
        self.setWindowTitle('Calibration')
        print(self.classification.exercises)
        self.buttons = []
        self.labels = []
        self.images = []
        self.exerciseLayouts = []
        self.recordReady = []
        exerciseContainer = QWidget()
        self.hLayout = QHBoxLayout()
        exerciseContainer.setLayout(self.hLayout)
        exerciseContainer.setStyleSheet(QStyles.backgroundGrey)
        exerciseContainer.setContentsMargins(10, 10, 10, 10)
        label = QLabel('Calibrating ' + self.patient.name)
        label.setStyleSheet(QStyles.labelStyle)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedHeight(30)
        font = label.font()
        font.setPointSize(15)
        label.setFont(font)

        layout.addWidget(label)
        readyButton = QPushButton('Ready')
        readyButton.setStyleSheet(QStyles.styledButtonStyle)
        readyButton.clicked.connect(self.calibrateReady)
        readyButton.setFixedSize(120, 35)
        self.progress = QProgressBar()

        bottomContainer = QHBoxLayout()
        bottomContainer.addWidget(self.progress)
        bottomContainer.addWidget(readyButton)
        bottomContainer.setAlignment(readyButton, Qt.AlignmentFlag.AlignRight)

        layout.addWidget(exerciseContainer)
        layout.addLayout(bottomContainer)
        self.recordThread = RecordThread(self.classification)
        self.trainThread = TrainThread(self.classification)
        self.trainThread.taskFinished.connect(self.onFinished)
        self.trained = False
        self.initUi()

    def onFinished(self):
        # Stop the progress
        self.progress.setRange(0, 1)
        self.progress.setValue(1)
        CustomDialog.message("Training information",
                             "Training model finished successfully.Accuracy: {} %, val. loss: {}"
                             .format(self.trainThread.acc, self.trainThread.loss),
                             "")
        self.trained = True

    def initUi(self):
        exerciseNames = [x.name for x in self.classification.exercises]
        for x, i in zip(exerciseNames, range(len(self.classification.exercises))):
            self.exerciseLayouts.append(QVBoxLayout())
            self.buttons.append(QPushButton('Record'))
            self.recordReady.append(False)
            image = QLabel()
            image.setPixmap(QPixmap(RESOURCES_PATH + 'frame.png'))
            image.setFixedHeight(100)
            label = QLabel(exerciseNames[i])
            label.setFixedHeight(30)
            font = label.font()
            font.setPointSize(12)
            label.setFont(font)
            self.labels.append(label)
            self.images.append(image)
            self.buttons[i].setFixedSize(100, 35)
            self.buttons[i].clicked.connect(functools.partial(self.onRecordExerciseButtonClicked, x, i))
            self.buttons[i].setStyleSheet(QStyles.outlineButtonStyle)
            self.exerciseLayouts[i].addWidget(self.labels[i])
            self.exerciseLayouts[i].addWidget(self.images[i])
            self.exerciseLayouts[i].addWidget(self.buttons[i])
            self.exerciseLayouts[i].setAlignment(self.labels[i], Qt.AlignmentFlag.AlignCenter)
            self.exerciseLayouts[i].setAlignment(self.images[i], Qt.AlignmentFlag.AlignCenter)
            self.exerciseLayouts[i].setAlignment(self.buttons[i], Qt.AlignmentFlag.AlignCenter)
            self.hLayout.addLayout(self.exerciseLayouts[i])

    def onRecordExerciseButtonClicked(self, name, index):
        print("Recording - ", name)
        if self.classification is not None:
            self.recordThread.exercise = name
            self.recordThread.taskFinished.connect(functools.partial(self.recordFinished,
                                                                     name,
                                                                     index), Qt.ConnectionType.SingleShotConnection)
            self.recordThread.start()
            self.recordReady[index] = False
            self.buttons[index].setStyleSheet(QStyles.recordStyle)
            self.images[index].setPixmap(QPixmap(RESOURCES_PATH + "frame.png"))

    def recordFinished(self, exercise, index):
        imagePath = "frame.png"
        if self.recordThread.result == 0:
            imagePath = "fail.png"
            self.buttons[index].setStyleSheet(QStyles.outlineButtonStyle)
        elif self.recordThread.result == 1:
            imagePath = "success.png"
            self.recordReady[index] = True
        else:
            print("None.")
        self.images[index].setPixmap(QPixmap(RESOURCES_PATH + imagePath))
        self.buttons[index].setStyleSheet(QStyles.outlineButtonStyle)

    def calibrateReady(self):
        if all(x == True for x in self.recordReady) and not self.trained:
            # print("All true!")
            self.classification.save_data()
            self.trainThread.start()
            self.progress.setRange(0, 0)
            # self.close()
        elif self.trained:
            self.accept()
        else:
            CustomDialog.message("Training information",
                                 "You must record all exercises to continue!",
                                 "")
            pass
