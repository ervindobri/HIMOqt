import functools

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QColor

from helpers.communication import SocketCommunication
from helpers.connection_state import ConnectionStatus
from ui.widgets.custom_ellipse_painter import CustomEllipse
from ui.widgets.custom_styles import QStyles

RED = QColor(255, 0, 0)
GREEN = QColor(0, 255, 50)


class ServerTab(QWidget):
    def __init__(self, parent = None):
        super(ServerTab, self).__init__(parent)
        layout = QVBoxLayout()
        self.setFixedSize(400, 300)
        self.setLayout(layout)

        statusLayoutContainer = QWidget()
        statusLayout = QHBoxLayout()

        label = QLabel("Connection status")
        label.setStyleSheet(QStyles.labelStyle)
        statusImage = CustomEllipse(10, RED)

        statusLayout.addWidget(label)
        statusLayout.addWidget(statusImage)
        statusLayoutContainer.setFixedSize(200, 50)
        statusLayoutContainer.setLayout(statusLayout)
        statusLayoutContainer.setStyleSheet(QStyles.borderedStyle)

        actionsLayout = QHBoxLayout()
        connectButton = QPushButton('Connect')
        listenButton = QPushButton('Listen')

        connectButton.setFixedSize(100, 50)
        connectButton.setStyleSheet(QStyles.outlineButtonStyle)
        connectButton.clicked.connect(functools.partial(self.setConnection, statusImage))
        listenButton.setFixedSize(100, 50)
        listenButton.setStyleSheet(QStyles.styledButtonStyle)
        listenButton.clicked.connect(self.startListen)


        actionsLayout.addWidget(connectButton)
        actionsLayout.addWidget(listenButton)

        layout.addWidget(statusLayoutContainer)
        layout.addLayout(actionsLayout)
        # layout.setAlignment(Qt.AlignTop)

        self.socketCommunication = SocketCommunication()
        self.connectionStatus = ConnectionStatus.DISCONNECTED
        print("Server tab init!")

    def setConnection(self, image):
        self.socketCommunication.Initialize()
        image.color = GREEN

    def startListen(self):
        self.socketCommunication.Listen()

