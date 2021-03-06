import json
import os
from os import listdir
from os.path import isfile, join
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, \
    QPushButton, QListWidget, QTabWidget, QMessageBox
from helpers.classification import Classification
from helpers.communication import LocalCommunication
from helpers.constants import PATIENTS_PATH, RESOURCES_PATH
from models.patient import Patient
from ui.widgets.custom.custom_styles import QStyles
from ui.widgets.dialogs.add_patient_dialog import AddPatientDialog
from ui.widgets.tabs.actions_tab import ActionsTab
from ui.widgets.tabs.server_tab import ServerTab
from ui.widgets.tabs.status_tab import StatusTab


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.deletePatientButton = QPushButton()
        self.classification = Classification(
            batch_size=25,
            epochs=500,
        )
        self.communication = LocalCommunication()

        self.patient = None
        self.selectedPatient = None
        self.addPatientButton = QPushButton('Add patient')
        self.tabLayout = QTabWidget()
        self.actionsTab = ActionsTab(
            classification=self.classification,
            communication=self.communication,
            patient=self.selectedPatient
        )
        self.statusTab = StatusTab()
        self.serverTab = ServerTab(
            classification=self.classification,
            communication=self.communication
        )

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
        # self.setStyleSheet("QWidget {background-color: white;} ")
        self.loadListItems()
        self.connections()


    def initUi(self):
        font = QLabel().font()
        font.setPointSize(12)
        self.tabLayout.addTab(self.actionsTab, "Actions")
        # self.tabLayout.addTab(self.statusTab, "Status")
        self.tabLayout.addTab(self.serverTab, "Server")
        # Status layout

        self.statusLayout.addWidget(self.statusLabel)
        self.statusLayout.addWidget(self.startButton)

        self.serverLayout.addWidget(self.serverLabel)
        self.infoLayout.addLayout(self.statusLayout)
        self.infoLayout.addLayout(self.serverLayout)

        icon = QIcon(RESOURCES_PATH + 'delete-blue.png')
        self.deletePatientButton.setFixedSize(35, 35)
        self.deletePatientButton.setStyleSheet(QStyles.outlineButtonStyle)
        self.deletePatientButton.setIcon(icon)
        self.deletePatientButton.setIconSize(QSize(30, 30))
        self.deletePatientButton.clicked.connect(self.openDeletePatientDialog)
        # TODO: delete patient data

        self.addPatientButton.setFixedHeight(35)
        self.addPatientButton.setStyleSheet(QStyles.styledButtonStyle)
        self.addPatientButton.setFont(font)
        self.addPatientButton.clicked.connect(self.openAddPatientDialog)
        # self.listLayout.setFixedHeight(self.window().height())
        listContainer = QVBoxLayout()
        actions = QHBoxLayout()
        actions.addWidget(self.addPatientButton)
        actions.addWidget(self.deletePatientButton)
        listContainer.addLayout(actions)
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

    def openDeletePatientDialog(self):
        # open messagebox
        if self.selectedPatient is not None:
            ret = QMessageBox.question(self,
                                       'Delete patient',
                                       "Are you sure you want to delete patient?",
                                       QMessageBox.StandardButton.Yes,
                                       QMessageBox.StandardButton.Cancel
                                       )

            if ret == QMessageBox.StandardButton.Yes:
                os.remove(PATIENTS_PATH + self.selectedPatient.name + '-' + self.selectedPatient.age + '.json')
                self.actionsTab.patient = None
                self.classification.set_patient()
                self.loadListItems()
                print('Patient deleted!')

    def openAddPatientDialog(self):
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
                print("Selectedpatient:", self.selectedPatient)

    def loadListItems(self):
        self.listLayout.clear()
        files = [f for f in listdir(PATIENTS_PATH) if isfile(join(PATIENTS_PATH, f))]
        files = [x.split('.')[0] for x in files]
        self.listLayout.addItems(files)

    def setStyles(self):
        self.tabLayout.setStyleSheet(QStyles.tabStyle)
        self.listLayout.setStyleSheet(QStyles.listStyle)
