from PyQt5.QtWidgets import QWidget, QVBoxLayout


class ServerTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setFixedSize(400, 300)
        self.setLayout(layout)
