import socket
import sys
import json

# PROTOCOL

# client->module typeID:0 GetConnectionStatus (asks module for its state, if its ready to send data)
#

# module->client typeID:1 ConnectionStatus (tells client if it's ready to send state or not, the module sends this to
# client when it receives a GetConnectionStatus request)

# client->module typeID:2 StartListen(tells module to send
# data about foot state continuously)

# module->client typeID:3 FootState(tells the state of the foot, this is sent as
# manny times as possible from the module if the client called StartListen)

# client->module typeID:4 StopListen(tells
# module to stop sending foot state continuously)
import win32file
import win32pipe

from helpers.connection_state import ConnectionStatus


class SocketCommunication:
    def __init__(self,
                 host: str = "localhost",
                 port: str = 9999
                 ):
        # self.HOST = host
        # self.port = port
        # self.address = (self.HOST, self.port)
        #
        # self.socket = None
        self.pipe = None
        self.handle = None

        self.connection_status = 0
        self.start_foot = False
        self.foot_state = 0
        self.responses = {
            "0": ('1', self.connection_status),
            "1": ("9", None),
            "2": ("3", self.foot_state),
            "3": ("9", None),
            "4": ("5", None)
        }
        # self.Initialize()
        # self.Listen()

    def initialize(self, name):
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create an UDP socket
        # self.socket.bind(self.address)
        # self.connection_status = ConnectionStatus.CONNECTED

        self.handle = win32file.CreateFile(
            r"\\.\pipe\{}".format(name),
            win32file.FD_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )
        self.pipe = win32pipe.SetNamedPipeHandleState(self.handle, win32pipe.PIPE_READMODE_BYTE, None, None)
        print("Initializing named pipe communication on pipe: ", name)
        return True

    def listen(self, exercise):
        try:
            # If streaming and we dont get a stop sign
            if self.start_foot:
                print("Streaming foot data!")
                self.SendMessage('2', exercise)
                return True, 'foot'
            else:
                self.start_foot = False
                resp1 = win32file.ReadFile(self.handle, 4)  # reading twice bcz we getting an empty message too
                response = win32file.ReadFile(self.handle, 1024)
                print("Read: ", resp1, " - and - ", response)
                message_list = list(response[1])  # taking the bytes as int list
                decoded = str(message_list[0]) + "".join(chr(x) for x in message_list[4:])  # taking
                # print(f"Read: {decoded}")
                message_type = decoded[0]
                self.SendMessage(message_type, exercise)
                return True, message_type
        except Exception as e:
            print(e)
            return False, -1

    def SendMessage(self, message_type, exercise):
        message = ""
        code, val = self.responses[message_type]
        if message_type == '0':

            message = chr(int(code)) + "\x00\x00\x00" + json.dumps({
                "Status": val
            })

        elif message_type == '2':
            self.start_foot = True
            message = chr(int(code)) + "\x00\x00\x00" + json.dumps({
                "Foot": exercise
            })
        print("Write: ", bytes(message.replace(" ", ""), encoding="raw_unicode_escape"))
        win32file.WriteFile(self.handle, bytes([10]))
        win32file.WriteFile(self.handle, bytes(message.replace(" ", ""), encoding="raw_unicode_escape"))

    def set_foot(self, state):
        self.responses["2"] = ("3", state)

    def stop_message_send(self):
        print("Stopped sending!")


if __name__ == '__main__':
    comm = SocketCommunication()
    comm.initialize("x")  # init -> set pipe name
    comm.listen()  # connect on gui
