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
        self.replyContainer = QLabel('last reply')
        label = QLabel("Connection status")
        statusImage = CustomEllipse(10, RED)
        actionsLayout = QHBoxLayout()
        self.pipeNameEdit = QLineEdit()

        label.setStyleSheet("font-weight: bold;")
        statusImage.setFixedSize(30, 15)
        statusLayout.addWidget(label)
        statusLayout.addWidget(statusImage)
        statusLayout.setAlignment(statusImage, Qt.Alignment.AlignRight)
        # statusLayoutContainer.setFixedSize(200, 50)
        statusLayoutContainer.setStyleSheet("background-color: #f0f0f0;")
        statusLayoutContainer.setLayout(statusLayout)

        self.connectButton = QPushButton('Connect')
        stopButton = QPushButton('Disconnect')

        self.connectButton.setFixedHeight(50)
        self.connectButton.setStyleSheet(QStyles.styledButtonStyle)
        self.connectButton.clicked.connect(functools.partial(self.setConnection, statusImage))
        stopButton.setFixedHeight(50)
        stopButton.setStyleSheet(QStyles.outlineButtonStyle)
        stopButton.clicked.connect(functools.partial(self.stopListen, statusImage))

        actionsLayout.addWidget(self.connectButton)
        actionsLayout.addWidget(stopButton)

        self.pipeNameEdit.setStyleSheet(QStyles.lineEditStyle)
        self.pipeNameEdit.setPlaceholderText('pipe name...')
        self.pipeNameEdit.setText('himo')

        layout.addWidget(self.pipeNameEdit)
        layout.addLayout(actionsLayout)
        layout.addWidget(statusLayoutContainer)
        # statusLayout.addWidget(self.replyContainer)
        font = self.replyContainer.font()
        font.setPointSize(15)
        self.replyContainer.setFont(font)
        # layout.addWidget(self.replyContainer)
        layout.setAlignment(self.pipeNameEdit, Qt.Alignment.AlignVCenter)
        layout.setAlignment(actionsLayout, Qt.Alignment.AlignVCenter)
        layout.setAlignment(statusLayoutContainer, Qt.Alignment.AlignBottom)

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
        ret = self.socketCommunication.initialize(self.pipeNameEdit.text())
        if ret:
            self.startListen()
            image.setColor(GREEN)
            image.setFixedSize(40, 15)

    def stopListen(self, image):
        self.communicationThread.terminate()
        image.setColor(RED)
        image.setFixedSize(30, 15)

    def startListen(self):
        self.communicationThread.start()
