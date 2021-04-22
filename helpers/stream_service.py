import time
from collections import deque
from multiprocessing import Lock
import myo
from helpers.constants import *


# To check if myo process is running
class MyoService:

    # Check if Myo Connect.exe process is running
    @staticmethod
    def check_if_process_running():
        try:
            for proc in psutil.process_iter():
                if proc.name() == PROC_NAME:
                    return True

            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print(PROC_NAME, " not running")

    # Restart myo connect.exe process if its not running
    @staticmethod
    def start_process():
        os.startfile(PROC_PATH)

    @staticmethod
    def restart_process():
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROC_NAME:
                proc.kill()
                # Wait a second
                time.sleep(1)

        while not MyoService.check_if_process_running():
            os.startfile(PROC_PATH)
            time.sleep(1)

        print("MYO Process started")
        instructions = "MYO App started"
        return True

class Listener(myo.DeviceListener):

    def __init__(self, n):
        self.n = n
        self.lock = Lock()
        self.emg_data_queue = deque(maxlen=n)

    def on_connected(self, event):
        print("Myo Connected")
        event.device.stream_emg(True)

    def get_emg_data(self):
        with self.lock:
            print("Locked")  # Ignore this

    def on_emg(self, event):
        with self.lock:
            self.emg_data_queue.append(event.emg)

            if len(list(self.emg_data_queue)) >= training_samples:
                data.append(list(self.emg_data_queue))
                self.emg_data_queue.clear()
                return False

class PrepareListener(myo.DeviceListener):
    def __init__(self, n):
        self.samples = n
        self._stop_requested = False

    def on_connected(self, event):
        print("--- Streaming EMG ---")
        event.device.stream_emg(True)

    def stop(self):
        self._stop_requested = True

    def on_emg(self, event):
        data.append(event.emg)
        if len(data) >= self.samples:
            return False


class PredictListener(myo.DeviceListener):
    def __init__(self, n):
        self.samples = n
        self.acceleration = None
        self.lock = Lock()

    def get_emg_data(self):
        return data


    def on_connected(self, event):
        print("--- Streaming EMG ---")
        event.device.stream_emg(True)

    def on_orientation(self, event):
        self.acceleration = event.acceleration

    def on_emg(self, event):
        with self.lock:
            data.append(event.emg)
            if len(data) >= self.samples:
                return False
