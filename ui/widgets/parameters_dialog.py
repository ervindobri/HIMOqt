import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

from classification import Classification
from constants import PREDEFINED_EXERCISES
from models.patient import Patient
from ui.widgets.custom_styles import QStyles


class ParametersDialog(QDialog):
    def __init__(self, parent,
                 classification: Classification = None,
                 patient: Patient = None
                 ):
        super(ParametersDialog, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.setFixedSize(300, 200)
        self.setLayout(layout)
        self.classification = classification
        selectLayout = QVBoxLayout()
        layout.addLayout(selectLayout)
        self.layouts = []
        self.labels = []
        self.combos = []
        for i in range(len(PREDEFINED_EXERCISES)):
            self.layouts.append(QHBoxLayout())
            self.labels.append(QLabel(PREDEFINED_EXERCISES[i].name))
            self.combos.append(QComboBox())
            self.layouts[i].addWidget(self.labels[i])
            self.combos[i].setPlaceholderText('Select reps')
            self.combos[i].setFixedSize(130, 50)
            # self.combos[i].lineEdit().setAlignment(Qt.AlignCenter)
            self.combos[i].addItems(PREDEFINED_EXERCISES[i].reps)
            self.combos[i].setStyleSheet(QStyles.comboStyle)
            self.combos[i].currentTextChanged.connect(functools.partial(self.repsSelected, i))
            self.layouts[i].addWidget(self.combos[i])
            self.combos[i].lineEdit().setAlignment(Qt.AlignCenter)
            selectLayout.addLayout(self.layouts[i])
            print(i)

        self.acceptButton = QPushButton('Accept')
        self.acceptButton.clicked.connect(functools.partial(self.onAcceptClicked, patient))
        layout.addWidget(self.acceptButton)
        self.parameters = {}

    def repsSelected(self, i):
        print(PREDEFINED_EXERCISES[i].name)
        self.parameters[PREDEFINED_EXERCISES[i].code] = self.combos[i].currentText()

    def onAcceptClicked(self, patient):
        patient.parameters = self.parameters
        print(patient.parameters)
        self.close()



