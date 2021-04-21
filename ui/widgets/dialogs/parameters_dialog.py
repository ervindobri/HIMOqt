import functools

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

from helpers.classification import Classification
from helpers.constants import PREDEFINED_EXERCISES, PREDEFINED_PARAMETERS
from models.patient import Patient
from ui.widgets.custom_styles import QStyles


class ParametersDialog(QDialog):
    def __init__(self, parent,
                 classification: Classification = None,
                 patient: Patient = None
                 ):
        super(ParametersDialog, self).__init__(parent)
        layout = QVBoxLayout(self)
        # self.setFixedSize(300, 200)
        self.setLayout(layout)
        self.classification = classification
        selectLayout = QVBoxLayout()
        layout.addLayout(selectLayout)
        self.layout = QVBoxLayout()
        self.label = QLabel('Repeats')
        self.combo = QComboBox()
        self.combo.currentTextChanged.connect(self.repsSelected)
        self.combo.setStyleSheet(QStyles.comboStyle)
        self.combo.addItems(PREDEFINED_PARAMETERS)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        selectLayout.addLayout(self.layout)

        self.acceptButton = QPushButton('Accept')
        self.acceptButton.clicked.connect(functools.partial(self.onAcceptClicked, patient))
        self.acceptButton.setStyleSheet(QStyles.styledButtonStyle)
        self.acceptButton.setFixedSize(100, 35)
        layout.addWidget(self.acceptButton)
        layout.setAlignment(self.acceptButton, Qt.Alignment.AlignCenter)
        self.parameters = {}

    def repsSelected(self):
        print(self.combo.currentText())

    def onAcceptClicked(self, patient):
        patient.parameters = self.parameters
        print(patient.parameters)
        self.close()



