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
from queue import Queue
from threading import Thread

import pywintypes
import win32file
import win32pipe
from winsys import constants, core, exc, utils

from helpers.connection_state import ConnectionStatus


class x_handles(exc.x_winsys):
    pass


WINERROR_MAP = {
}
wrapped = exc.wrapper(WINERROR_MAP, x_handles)


class SocketCommunication:
    def __init__(self,
                 host: str = "localhost",
                 port: str = 9999
                 ):
        self.pipe = None
        self.handle = None

        self.connection_status = 0
        self.start_foot = False
        self.foot_state = 0
        self.responses = {
            "0": ('1', self.connection_status),  # send connection state
            "1": ("99", None),
            "2": ("3", self.foot_state),  # start listen
            "3": ("99", None),
            "4": ("99", None),  # stop listen
            "5": ("99", None),
            "6": ("99", None)
        }
        # self.Initialize()
        # self.Listen()

    def close(self):
        if self.handle is not None:
            self.handle.close()
            self.pipe.close()
            print("Pipe closed!")

    def initialize(self, name):
        try:
            if self.handle is None:
                self.handle = win32file.CreateFile(
                    r"\\.\pipe\{}".format(name),
                    win32file.FD_READ | win32file.GENERIC_WRITE | win32pipe.PIPE_WAIT,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None
                )
                self.pipe = win32pipe.SetNamedPipeHandleState(self.handle,
                                                              win32pipe.PIPE_READMODE_BYTE,
                                                              None,
                                                              None)

            print("Initializing named pipe communication on pipe: ", name)
            return True
        except Exception as e:
            print("Pipe error:", e)
            return False

    def read(self):
        res, resp1 = win32file.ReadFile(self.handle, 4)  # length?
        res, resp2 = win32file.ReadFile(self.handle, 1024)  # data
        # print(f"Read: {resp2}")
        message_list = list(resp2)  # taking the bytes as int list
        decoded = str(message_list[0]) + "".join(chr(x) for x in message_list[4:])  # taking
        return decoded

    def listen(self, exercise):
        try:
            data = self.read()
            message_type = data[0]
            self.start_foot = message_type == '5'  # stop if stopListen

            # Stream foot data continuously
            if self.start_foot:
                self.SendMessage('2', int(exercise))
                return True, 'foot'
            else:
                self.SendMessage(message_type, int(exercise))
                return True, message_type
        except Exception as e:
            print(e)
            return False, -1

    def SendMessage(self, message_type, exercise):
        code, val = self.responses[message_type]
        message = chr(int(code)) + "\x00\x00\x00"
        if val is not None:
            if message_type == '0':

                message += json.dumps({
                    "Status": val
                })
            elif message_type == '2':
                self.start_foot = True
                message += json.dumps({
                    "State": exercise
                })
            # print("Write: ", list(bytes(message.replace(" ", ""),
            #                             encoding="raw_unicode_escape")))
            print(message)
            win32file.WriteFile(self.handle, bytes([len(message.replace(" ", "")), 0, 0, 0]))
            win32file.WriteFile(self.handle, bytes(message.replace(" ", ""),
                                                   encoding="raw_unicode_escape"))

    def set_foot(self, state):
        self.responses["2"] = ("3", state)

    def stop_message_send(self):
        print("Stopped sending!")


if __name__ == '__main__':
    comm = SocketCommunication()
    comm.initialize("x")  # init -> set pipe name
    comm.listen(0)  # connect on gui
