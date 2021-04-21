import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt6.QtCore import Qt, QRect


class CustomEllipse(QWidget):

    def __init__(self, size, color):
        super().__init__()
        self.size = size
        self.color = color
        # self.initUI()

    # def initUI(self):

    # TODO repaint green

    def paintEvent(self, event):
        px = QPixmap(self.size, self.size)
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(self.color))
        qp.setPen(QColor(self.color))
        qp.drawEllipse(px.rect())
        qp.end()