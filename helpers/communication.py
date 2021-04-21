import socket
import sys
import json


# PROTOCOL

# client->module typeID:0 GetConnectionStatus (asks module for its state, if its ready to send data)

# module->client typeID:1 ConnectionStatus (tells client if it's ready to send state or not, the module sends this to
# client when it receives a GetConnectionStatus request)

# client->module typeID:2 StartListen(tells module to send
# data about foot state continuously)

# module->client typeID:3 FootState(tells the state of the foot, this is sent as
# manny times as possible from the module if the client called StartListen)

# client->module typeID:4 StopListen(tells
# module to stop sending foot state continuously)
from helpers.connection_state import ConnectionStatus


class SocketCommunication:
    def __init__(self,
                 host: str = "localhost",
                 port: str = 9999
                 ):
        self.HOST = host
        self.port = port
        self.address = (self.HOST, self.port)

        self.socket = None
        self.connection_status = 0
        self.foot_state = 0
        self.responses = {
            "0": ('1', self.connection_status),
            "2": ("3", self.foot_state),
            "4": ("4", None)
        }
        # self.Initialize()
        # self.Listen()

    def Initialize(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create an UDP socket
        self.socket.bind(self.address)
        self.connection_status = ConnectionStatus.CONNECTED
        print("Initializing socket communication!")


    def Listen(self):
        while True:
            bytesAddressPair = self.socket.recvfrom(1024)
            message_type = bytesAddressPair[0].split('{')[0]
            clientMsg = "Message from Client:{}".format(message_type)
            clientIP = "Client IP Address:{}".format(self.address)

            print(clientMsg)
            print(clientIP)

            # Sending a reply to client
            self.SendMessage(message_type, self.responses[message_type])

    def SendMessage(self, message_type, status):
        message = ""
        if message_type == '1':
            message = message_type + json.dumps({
                "Status": status
            })

        elif message_type == '3':
            message = message_type + json.dumps({
                "Foot": status
            })
        print(message)
        # self.socket.sendto(message, address)

    def StopSendMessage(self):
        print("Stopped sending!")



