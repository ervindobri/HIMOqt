from PyQt5.QtWidgets import QDialog, QVBoxLayout

from classification import Classification


class CalibrateDialog(QDialog):
    def __init__(self, parent, classification: Classification = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setFixedSize(500, 300)
        self.setLayout(layout)
        self.classification = classification
