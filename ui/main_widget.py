import json
from os import listdir
from os.path import isfile, join

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QTabWidget

from helpers.classification import Classification
from helpers.constants import PATIENTS_PATH
from models.patient import Patient
from ui.widgets.custom.custom_styles import QStyles
from ui.widgets.dialogs.add_patient_dialog import AddPatientDialog
from ui.widgets.tabs.actions_tab import ActionsTab
from ui.widgets.tabs.server_tab import ServerTab
from ui.widgets.tabs.status_tab import StatusTab


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.addPatientButton = QPushButton('Add patient')
        self.classification = Classification(
            batch_size=25,
        )
        self.patient = None

        # self.patient = self.getPatientInfo()
        # self.classification.set_patient(self.patient)
        self.selectedPatient = None

        self.tabLayout = QTabWidget()
        self.actionsTab = ActionsTab(classification=self.classification, patient=self.selectedPatient)
        self.statusTab = StatusTab()
        self.serverTab = ServerTab()

        self.contentLayout = QVBoxLayout()
        self.listLayout = QListWidget()

        self.serverLabel = QLabel("Server")
        self.startButton = QPushButton("Start")
        self.statusLabel = QLabel("Status")
        self.layout = QHBoxLayout(self)
        self.actionLayout = QVBoxLayout()
        self.infoLayout = QHBoxLayout()
        self.statusLayout = QVBoxLayout()
        self.serverLayout = QVBoxLayout()


        self.initUi()
        self.setStyles()
        self.setStyleSheet("QWidget {background-color: white;} ")
        self.loadListItems()
        self.connections()



    def initUi(self):
        self.tabLayout.addTab(self.actionsTab, "Actions")
        self.tabLayout.addTab(self.statusTab, "Status")
        self.tabLayout.addTab(self.serverTab, "Server")
        # Status layout

        self.statusLayout.addWidget(self.statusLabel)
        self.statusLayout.addWidget(self.startButton)

        self.serverLayout.addWidget(self.serverLabel)
        self.infoLayout.addLayout(self.statusLayout)
        self.infoLayout.addLayout(self.serverLayout)

        self.addPatientButton.setFixedHeight(35)
        self.addPatientButton.setStyleSheet(QStyles.styledButtonStyle)
        self.addPatientButton.clicked.connect(self.openAddPatientDialog)
        # self.listLayout.setFixedHeight(self.window().height())
        listContainer = QVBoxLayout()
        listContainer.addWidget(self.addPatientButton)
        listContainer.addWidget(self.listLayout)
        self.listLayout.setFixedWidth(200)
        self.listLayout.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        contentWidget = QWidget()
        contentWidget.setStyleSheet(QStyles.backgroundWhite)
        self.contentLayout.addWidget(self.tabLayout)
        contentWidget.setLayout(self.contentLayout)

        self.layout.addLayout(listContainer)
        self.layout.addWidget(contentWidget)

    def connections(self):

        self.listLayout.clicked.connect(self.listClicked)


    def openAddPatientDialog(self):
        # todo: open dialog
        dialog = AddPatientDialog(self,
                                  self.patient
                                  )
        dialog.exec()
        self.loadListItems()



    # Connect when list element is clicked, set patient and load back info
    def listClicked(self, index):
        item = self.listLayout.currentItem()
        if self.classification is not None:
            name, age = item.text().split('-')
            self.classification.subject_name = name
            self.classification.subject_age = age

            # Load information
            with open(PATIENTS_PATH + item.text() + '.json') as file:
                dict = json.load(file)
                patient = Patient(
                    dict['id'],
                    dict['name'],
                    dict['age'],
                    dict['parameters'],
                )
                self.selectedPatient = patient
                self.actionsTab.patient = patient
                self.classification.set_patient(patient)
                print(self.selectedPatient)

    def onLoadButtonClicked(self):
        # TODO: load back parameters and info
        pass

    def loadListItems(self):
        self.listLayout.clear()
        files = [f for f in listdir(PATIENTS_PATH) if isfile(join(PATIENTS_PATH, f))]
        files = [x.split('.')[0] for x in files]
        self.listLayout.addItems(files)

    def setStyles(self):
        self.tabLayout.setStyleSheet(QStyles.tabStyle)
        self.listLayout.setStyleSheet(QStyles.listStyle)

    def onSubjectNameSet(self):
        # todo open dialog with calibration
        self.classification.subject_name = self.nameInput.text()
        print("Setting name.")

    def onSubjectAgeSet(self):
        # todo open dialog with calibration
        self.classification.subject_age = self.ageInput.text()
        print("Setting age:", self.classification.subject_age)
