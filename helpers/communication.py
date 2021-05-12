import json
import win32file
import win32pipe


class LocalCommunication:
    def __init__(self,
                 host: str = "localhost",
                 port: str = 9999
                 ):
        self.pipe = None

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
        if self.pipe is not None:
            self.pipe.close()
            print("Pipe closed!")

    def initialize(self, name):
        try:
            if self.pipe is None:
                self.pipe = win32pipe.CreateNamedPipe(
                    r'\\.\pipe\{}'.format(name),
                    win32pipe.PIPE_ACCESS_DUPLEX,
                    win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT,
                    1,
                    65536,
                    65536,
                    0,
                    None
                )
                win32pipe.ConnectNamedPipe(self.pipe, None)
            print("Initializing named pipe communication on pipe: ", name)
            return True
        except Exception as e:
            print("Pipe error:", e)
            return False

    def read(self):
        res, resp1 = win32file.ReadFile(self.pipe, 4)  # length?
        res, resp2 = win32file.ReadFile(self.pipe, 1024)  # data
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
                self.send_message('2', int(exercise))
                return True, 'foot'
            else:
                self.send_message(message_type, int(exercise))
                return True, message_type
        except Exception as e:
            print(e)
            return False, -1

    def send_message(self, message_type, exercise=None):
        code, val = self.responses[message_type]
        message = chr(int(code)) + "\x00\x00\x00"
        if val is not None:
            if message_type == '0':

                message += json.dumps({
                    "Status": val
                })
            elif message_type == '2':
                message += json.dumps({
                    "State": exercise
                })
            win32file.WriteFile(self.pipe, bytes([len(message.replace(" ", "")), 0, 0, 0]))
            win32file.WriteFile(self.pipe, bytes(message.replace(" ", ""),
                                                 encoding="raw_unicode_escape"))

    def start_listen(self):
        try:
            print("Starting comm thread!")
            self.connection_status = 2
            self.responses['0'] = ('1', self.connection_status)
            self.send_message('0')
        except:
            pass

    def stop_listen(self):
        try:
            print("stopping listening")
            self.connection_status = 1
            self.responses['0'] = ('1', self.connection_status)
            self.send_message('0')
        except:
            pass


if __name__ == '__main__':
    comm = LocalCommunication()
    comm.initialize("x")  # init -> set pipe name
    comm.listen(0)  # connect on gui
