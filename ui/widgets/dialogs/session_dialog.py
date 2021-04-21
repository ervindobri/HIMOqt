from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QPushButton


class SessionDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setFixedSize(500, 300)
        self.setLayout(self.layout)

        self.tabLayout = QTabWidget()
        self.parametersTab = QWidget()
        self.exercisesTab = QWidget()
        self.resultsTab = QWidget()

        self.layout.addWidget(self.tabLayout)
        self.initUi()

    def initUi(self):
        self.tabLayout.addTab(self.parametersTab, "Parameters")
        self.tabLayout.addTab(self.exercisesTab, "Exercises")
        self.tabLayout.addTab(self.resultsTab, "Results")
        self.tabLayout.tabBar().setFixedWidth(250)

        self.setParametersTab()
        self.setExercisesTab()
        self.setResultsTab()

    def setParametersTab(self):
        layout = QVBoxLayout()
        self.parametersTab.setLayout(layout)
        startButton = QPushButton('Start')
        startButton.clicked.connect(self.startSession)
        layout.addWidget(startButton)

    def startSession(self):
        self.tabLayout.setCurrentIndex(1)

    def setExercisesTab(self):
        pass

    def setResultsTab(self):
        pass