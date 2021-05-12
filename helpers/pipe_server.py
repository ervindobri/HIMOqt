import time
import win32file
import win32pipe


def pipe_server(name):
    print("pipe server")
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\{}'.format(name),
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_NOWAIT,
        1,
        65536,
        65536,
        0,
        None)
    try:
        print("waiting for client")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("Client connected. Waiting for messages")
        some_data = str.encode(f"{count}")
        win32file.WriteFile(pipe, some_data)
        print("Data sent!")
        while count < 10:
            win32file.WriteFile(pipe, b'\x00\x00\x00\x00{}')
            read = win32file.ReadFile(pipe, 1024)
            print(read)
            time.sleep(1)
            count += 1

        print("finished now")
    finally:
        win32file.CloseHandle(pipe)


if __name__ == '__main__':
    pipe_server("pipe")
