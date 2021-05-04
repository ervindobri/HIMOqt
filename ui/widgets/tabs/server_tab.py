import functools

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QColor

from helpers.communication import SocketCommunication
from helpers.connection_state import ConnectionStatus
from ui.threads.comm_thread import CommThread
from ui.widgets.custom.custom_ellipse_painter import CustomEllipse
from ui.widgets.custom.custom_styles import QStyles

RED = QColor(255, 0, 0)
GREEN = QColor(0, 255, 50)


class ServerTab(QWidget):
    def __init__(self,
                 classification=None,
                 parent=None):
        super(ServerTab, self).__init__(parent)
        layout = QVBoxLayout()
        self.setFixedSize(400, 300)
        self.setLayout(layout)

        statusLayoutContainer = QWidget()
        statusLayout = QHBoxLayout()

        label = QLabel("Connection status")
        label.setStyleSheet("font-weight: bold;")
        statusImage = CustomEllipse(10, RED)

        statusLayout.addWidget(label)
        statusLayout.addWidget(statusImage)
        statusLayout.setAlignment(label, Qt.Alignment.AlignCenter)
        statusLayout.setAlignment(statusImage, Qt.Alignment.AlignCenter)
        statusLayoutContainer.setFixedSize(200, 50)
        statusLayoutContainer.setLayout(statusLayout)
        # statusLayoutContainer.setStyleSheet()

        actionsLayout = QHBoxLayout()
        self.connectButton = QPushButton('Connect')
        listenButton = QPushButton('Listen')

        self.connectButton.setFixedSize(100, 50)
        self.connectButton.setStyleSheet(QStyles.outlineButtonStyle)
        self.connectButton.clicked.connect(functools.partial(self.setConnection, statusImage))
        listenButton.setFixedSize(100, 50)
        listenButton.setStyleSheet(QStyles.styledButtonStyle)
        listenButton.clicked.connect(self.startListen)

        actionsLayout.addWidget(self.connectButton)
        actionsLayout.addWidget(listenButton)

        self.pipeNameEdit = QLineEdit()
        self.pipeNameEdit.setStyleSheet(QStyles.lineEditStyle)
        self.pipeNameEdit.setPlaceholderText('pipe name...')
        layout.addWidget(self.pipeNameEdit)
        layout.addLayout(actionsLayout)
        layout.addWidget(statusLayoutContainer)
        self.replyContainer = QLabel('last reply')
        layout.addWidget(self.replyContainer)
        layout.setAlignment(statusLayoutContainer, Qt.Alignment.AlignCenter)
        # layout.setAlignment(Qt.AlignTop)

        self.socketCommunication = SocketCommunication()
        self.classification = classification
        self.connectionStatus = ConnectionStatus.DISCONNECTED

        self.communicationThread = CommThread(
            self.socketCommunication,
            self.classification
        )
        self.communicationThread.replySignal.connect(self.readReply)
        print("Server tab init!")

    def readReply(self, value):
        self.replyContainer.setText(value)

    def setConnection(self, image):
        self.socketCommunication.initialize(self.pipeNameEdit.text())
        image.color = GREEN
        # self.connectButton.setDisabled(True)

    def stopListen(self):
        print("Quitting comm. thread")
        self.communicationThread.quit()

    def startListen(self):
        print("Quitting comm. thread")
        self.communicationThread.start()
