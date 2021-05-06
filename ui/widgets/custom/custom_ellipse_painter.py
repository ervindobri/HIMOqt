import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt6.QtCore import Qt, QRect, pyqtSignal, pyqtSlot


class CustomEllipse(QWidget):

    def __init__(self, size, color):
        super().__init__()
        self.size = size
        self.color = color

    # @pyqtSlot
    def setColor(self, color):
        self.color = color

    def paintEvent(self, event):
        px = QPixmap(self.size, self.size)
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(self.color))
        qp.setPen(QColor(self.color))
        qp.drawEllipse(px.rect())
        qp.end()
