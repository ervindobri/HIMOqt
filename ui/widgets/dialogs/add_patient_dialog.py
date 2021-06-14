import json
import os
from os import listdir
from os.path import isfile, join

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox

from helpers.constants import PATIENTS_PATH, DATA_PATH, PREDEFINED_PARAMETERS
from models.patient import Patient
from ui.widgets.dialogs.show_dialog import CustomDialog
from ui.widgets.custom.custom_styles import QStyles


class AddPatientDialog(QDialog):
    def __init__(self, parent=None,
                 patient: Patient = None
                 ):
        super(AddPatientDialog, self).__init__(parent)
        self.setWindowTitle('New Patient')

        self.inputLayout = QVBoxLayout()
        self.setLayout(self.inputLayout)

        self.nameInputLayout = QHBoxLayout()
        self.ageInputLayout = QHBoxLayout()
        self.paramLayout = QHBoxLayout()

        self.nameLabel = QLabel("Name")
        self.ageLabel = QLabel("Age")
        self.paraLabel = QLabel('Repeats')

        self.nameInput = QLineEdit()
        self.ageInput = QLineEdit()
        self.paraCombo = QComboBox()

        self.saveButton = QPushButton("Save")

        self.patient = patient
        if patient is None:
            self.patient = self.getPatientInfo()

        self.initUi()
        self.setStyles()

    def setStyles(self):
        self.nameLabel.setStyleSheet(QStyles.labelStyle)
        self.ageLabel.setStyleSheet(QStyles.labelStyle)
        self.nameInput.setStyleSheet(QStyles.lineEditStyle)
        self.ageInput.setStyleSheet(QStyles.lineEditStyle)
        self.saveButton.setStyleSheet(QStyles.styledButtonStyle)
        self.paraLabel.setStyleSheet(QStyles.labelStyle)

    def getPatientId(self):
        file = [f for f in listdir(PATIENTS_PATH) if isfile(join(PATIENTS_PATH, f))]
        id = len(file) + 1
        return id

    def getPatientInfo(self):
        patient = Patient(
            self.getPatientId(),
            self.nameInput.text(),
            self.ageInput.text(),
        )
        return patient

    def initUi(self):
        # Input layout and list
        self.nameLabel.setFixedSize(100, 30)
        self.ageLabel.setFixedSize(100, 30)
        font = self.nameInput.font()
        font.setPointSize(13)  # change it's size
        self.nameInput.setFont(font)
        self.nameInput.setPlaceholderText('Ervin')
        self.nameInput.setText('Ervin')
        self.nameInput.setFixedWidth(200)
        # self.saveButton.setFixedSize(100, 30)
        self.saveButton.setFont(font)
        self.saveButton.setFixedHeight(30)

        self.nameInputLayout.addWidget(self.nameLabel)
        self.nameInputLayout.addWidget(self.nameInput)
        self.nameInputLayout.setAlignment(self.nameLabel, Qt.AlignmentFlag.AlignLeft)
        self.nameInputLayout.setAlignment(self.nameInput, Qt.AlignmentFlag.AlignRight)

        # To allow only int
        onlyInt = QIntValidator()
        self.ageInput.setValidator(onlyInt)
        self.ageInput.setFont(font)
        self.ageInput.setPlaceholderText('5')
        self.ageInput.setText('5')
        self.ageInput.setFixedWidth(200)

        self.ageInputLayout.addWidget(self.ageLabel)
        self.ageInputLayout.addWidget(self.ageInput)
        self.ageInputLayout.setAlignment(self.ageLabel, Qt.AlignmentFlag.AlignLeft)
        self.ageInputLayout.setAlignment(self.ageInput, Qt.AlignmentFlag.AlignRight)

        self.paraCombo.setFixedSize(200, 30)
        self.paraCombo.setFont(font)

        self.paraCombo.addItems(PREDEFINED_PARAMETERS)
        self.paraCombo.setStyleSheet(QStyles.comboStyle)

        self.paraCombo.currentTextChanged.connect(self.repsSelected)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.paramLayout.addWidget(self.paraLabel)
        self.paramLayout.addWidget(self.paraCombo)

        self.inputLayout.addLayout(self.nameInputLayout)
        self.inputLayout.addLayout(self.ageInputLayout)
        self.inputLayout.addLayout(self.paramLayout)
        self.inputLayout.addWidget(self.saveButton)
        self.inputLayout.setContentsMargins(15, 15, 15, 10)

    def repsSelected(self):
        print(self.paraCombo.currentText())
        self.patient.parameters = self.paraCombo.currentText()

    def onSaveButtonClicked(self):
        self.patient.id = self.getPatientId()
        self.patient.name = self.nameInput.text()
        self.patient.age = self.ageInput.text()
        self.patient.parameters = self.paraCombo.currentText()
        patient = self.patient
        print(patient)
        if patient.name != "" and patient.age != "" and patient.parameters is not None:
            with open(PATIENTS_PATH + patient.name + '-' + str(patient.age) + '.json', 'w') as f:
                content = {
                    'id': patient.id,
                    'name': patient.name,
                    'age': patient.age,
                    'parameters': patient.parameters

                }
                json.dump(content, f)
                f.close()
            self.close()
            if os.path.exists(DATA_PATH + str(patient.id - 1) + '.xyz'):
                os.rename(DATA_PATH + str(patient.id - 1) + '.xyz', DATA_PATH + str(patient.id) + '.xyz')
        else:
            print("Set up patient data.")
            CustomDialog.message(
                "Saving patient data",
                "Patient set up is not complete.",
                "Did you forget to set parameters?")
