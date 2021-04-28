from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit, QToolButton, QStyle


class ButtonLineEdit(QLineEdit):
    buttonClicked = QtCore.pyqtSignal(bool)

    def __init__(self, button_text, parent=None):
        super(ButtonLineEdit, self).__init__(parent)

        self.button = QToolButton(self)
        # self.button.setIcon(QIcon(icon_file))
        # self.button.setMinimumSize(30, 50)
        # self.button.setMaximumSize(50, 150)
        self.button.setFixedSize(100, 30)
        self.button.setText(button_text)
        # self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        self.button.clicked.connect(self.buttonClicked.emit)

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        # self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth * 2 + 2),
                            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth * 2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.size()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width() - 10,
                         (self.rect().bottom() - buttonSize.height() + 1) / 2)
        super(ButtonLineEdit, self).resizeEvent(event)

    def setButtonStyle(self, stylesheet):
        self.button.setStyleSheet(stylesheet)
