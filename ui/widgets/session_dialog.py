from PyQt5.QtWidgets import QDialog, QVBoxLayout


class SessionDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setFixedSize(500, 300)
        self.setLayout(layout)
