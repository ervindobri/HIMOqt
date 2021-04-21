from PyQt6.QtWidgets import QWidget, QVBoxLayout


class StatusTab(QWidget):
    def __init__(self, parent=None):
        super(StatusTab, self).__init__(parent)
        layout = QVBoxLayout()
        self.setFixedSize(400, 300)
        self.setLayout(layout)
