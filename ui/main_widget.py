import json
import os
from os import listdir
from os.path import isfile, join

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QListWidget, QTabWidget, \
    QToolButton

from classification import Classification
from constants import PATIENTS_PATH, DATA_PATH
from models.patient import Patient
from ui.widgets.custom_button import ButtonLineEdit
from ui.widgets.custom_styles import QStyles
from ui.widgets.parameters_dialog import ParametersDialog
from ui.widgets.separators import QHSeparationLine
from ui.widgets.tabs.actions_tab import ActionsTab
from ui.widgets.tabs.server_tab import ServerTab
from ui.widgets.tabs.status_tab import StatusTab


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.selectParametersButton = QPushButton('Set Parameters')
        self.loadButton = QPushButton("Load")
        self.saveButton = QPushButton("Save")
        self.classification = Classification(
            batch_size=25,
        )


        self.tabLayout = QTabWidget()
        self.actionsTab = ActionsTab(self, self.classification)
        self.statusTab = StatusTab(self)
        self.serverTab = ServerTab(self)

        self.contentLayout = QVBoxLayout()
        self.listLayout = QListWidget()
        self.nameInputLayout = QHBoxLayout()
        self.ageInputLayout = QHBoxLayout()
        self.serverLabel = QLabel("Server")
        self.startButton = QPushButton("Start")
        self.statusLabel = QLabel("Status")
        self.layout = QHBoxLayout(self)
        self.inputLayout = QVBoxLayout()
        self.actionLayout = QVBoxLayout()
        self.infoLayout = QHBoxLayout()
        self.statusLayout = QVBoxLayout()
        self.serverLayout = QVBoxLayout()

        self.nameLabel = QLabel("Name")
        self.ageLabel = QLabel("Age")

        self.nameInput = QLineEdit()
        self.ageInput = QLineEdit()

        self.patient = self.getPatientInfo()

        self.initUi()
        self.setStyles()
        self.setStyleSheet("QWidget {background-color: white;} ")
        self.loadListItems()
        self.connections()

    def initUi(self):
        # Input layout and list
        self.nameLabel.setFixedSize(100, 30)
        self.ageLabel.setFixedSize(100, 30)
        font = self.nameInput.font()
        font.setPointSize(12)  # change it's size
        self.nameInput.setFont(font)
        self.nameInput.setPlaceholderText('Ervin')
        self.nameInput.setFixedWidth(200)
        # self.saveButton.setFixedSize(100, 30)
        self.selectParametersButton.setFixedSize(100, 30)
        self.saveButton.setFixedHeight(30)
        self.loadButton.setFixedHeight(30)

        self.nameInputLayout.addWidget(self.nameLabel)
        self.nameInputLayout.addWidget(self.nameInput)
        self.nameInputLayout.setAlignment(self.nameLabel, Qt.AlignLeft)
        self.nameInputLayout.setAlignment(self.nameInput, Qt.AlignLeft)
        self.nameInputLayout.addWidget(self.selectParametersButton)

        # To allow only int
        onlyInt = QIntValidator()
        self.ageInput.setValidator(onlyInt)
        self.ageInput.setFont(font)
        self.ageInput.setPlaceholderText('5')
        self.ageInput.setFixedWidth(200)

        # self.loadButton.setFixedSize(100, 30)
        self.ageInputLayout.addWidget(self.ageLabel)
        self.ageInputLayout.addWidget(self.ageInput)
        widget = QWidget()
        widget.setFixedSize(100, 30)
        self.ageInputLayout.setAlignment(self.ageLabel, Qt.AlignLeft)
        self.ageInputLayout.setAlignment(self.ageInput, Qt.AlignLeft)
        self.ageInputLayout.addWidget(widget)

        self.selectParametersButton.setFixedHeight(30)
        self.selectParametersButton.setFocusPolicy(Qt.NoFocus)
        self.inputLayout.addLayout(self.nameInputLayout)
        self.inputLayout.addLayout(self.ageInputLayout)
        self.inputLayout.addWidget(self.saveButton)
        self.inputLayout.addWidget(self.loadButton)
        self.inputLayout.setContentsMargins(3, 3, 3, 10)
        # Tab layout

        self.tabLayout.addTab(self.actionsTab, "Actions")
        self.tabLayout.addTab(self.statusTab, "Status")
        self.tabLayout.addTab(self.serverTab, "Server")
        self.tabLayout.tabBar().setFixedWidth(250)
        # Status layout

        self.statusLayout.addWidget(self.statusLabel)
        self.statusLayout.addWidget(self.startButton)

        self.serverLayout.addWidget(self.serverLabel)
        self.infoLayout.addLayout(self.statusLayout)
        self.infoLayout.addLayout(self.serverLayout)

        # self.listLayout.setFixedHeight(self.window().height())
        self.listLayout.setFixedWidth(200)
        self.listLayout.setFocusPolicy(Qt.NoFocus)

        contentWidget = QWidget()
        contentWidget.setStyleSheet(QStyles.backgroundWhite)
        self.contentLayout.addLayout(self.inputLayout)
        self.contentLayout.addWidget(QHSeparationLine())
        self.contentLayout.addWidget(self.tabLayout)
        contentWidget.setLayout(self.contentLayout)

        self.layout.addWidget(self.listLayout)
        self.layout.addWidget(contentWidget)

    def connections(self):
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.loadButton.clicked.connect(self.onLoadButtonClicked)
        self.selectParametersButton.clicked.connect(self.onSelectParameters)

    def onSelectParameters(self):
        dialog = ParametersDialog(self,
                                  self.classification,
                                  self.patient
                                  )
        dialog.exec_()

    def getPatientInfo(self):
        file = [f for f in listdir(PATIENTS_PATH) if isfile(join(PATIENTS_PATH, f))]
        id = len(file) + 1
        patient = Patient(
            id,
            self.nameInput.text(),
            self.ageInput.text(),
        )
        return patient

    def onSaveButtonClicked(self):

        self.patient.name = self.nameInput.text()
        self.patient.age = self.ageInput.text()
        patient = self.patient
        if patient.name != "" and patient.age != "" and patient.parameters is not None:
            with open(PATIENTS_PATH + patient.name + '-' + str(patient.age) + '.json', 'w') as f:
                content = {
                    'id': patient.id,
                    'name': patient.name,
                    'age': patient.age,
                    'parameters':  patient.parameters

                }
                json.dump(content, f)
                f.close()
            if os.path.exists(DATA_PATH + str(patient.id-1) + '.xyz'):
                os.rename(DATA_PATH + str(patient.id-1) + '.xyz', DATA_PATH + str(patient.id) + '.xyz')
            self.loadListItems()
        else:
            print("Set up patient data.")

    def onLoadButtonClicked(self):
        pass


    def loadListItems(self):
        self.listLayout.clear()
        files = [f for f in listdir(PATIENTS_PATH) if isfile(join(PATIENTS_PATH, f))]
        files = [x.split('.')[0] for x in files]
        self.listLayout.addItems(files)

    def setStyles(self):
        self.saveButton.setStyleSheet(QStyles.styledButtonStyle)
        self.loadButton.setStyleSheet(QStyles.outlineButtonStyle)
        self.selectParametersButton.setStyleSheet(QStyles.styledButtonStyle)
        self.tabLayout.setStyleSheet(QStyles.tabStyle)
        self.nameLabel.setStyleSheet(QStyles.labelStyle)
        self.ageLabel.setStyleSheet(QStyles.labelStyle)
        self.nameInput.setStyleSheet(QStyles.lineEditStyle)
        self.ageInput.setStyleSheet(QStyles.lineEditStyle)
        self.listLayout.setStyleSheet(QStyles.listStyle)

    def onSubjectNameSet(self):
        # todo open dialog with calibration
        self.classification.subject_name = self.nameInput.text()
        print("Setting name.")

    def onSubjectAgeSet(self):
        # todo open dialog with calibration
        self.classification.subject_age = self.ageInput.text()
        print("Setting age:", self.classification.subject_age)
