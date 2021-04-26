import os

import psutil
from pynput.keyboard import Key, KeyCode
from models.exercise import Exercise

data = []
training_samples = 500
samples = 50

PROC_NAME = "Myo Connect.exe"
PROC_PATH = ""

for proc in psutil.process_iter():
    if proc.name() == PROC_NAME:
        PROC_PATH = proc.exe()

RESOURCES_PATH = os.getcwd() + '\\resources\\'
DATA_PATH = os.getcwd() + '\\data\\'
PATIENTS_PATH = os.getcwd() + '\\data\\patients\\'
RESULT_PATH = os.getcwd() + '\\data\\results\\'
TRAINING_DATA_PATH = RESULT_PATH + '\\training_data\\'
RAW_DATA_PATH = RESULT_PATH + 'raw_data\\'
TRAINING_MODEL_PATH = RESULT_PATH + '\\training_model\\'
FIGURES_PATH = RESULT_PATH + '\\training_figures\\'
KEYS = {
    "UP": Key.up,
    "DOWN": Key.down,
    "LEFT": Key.left,
    "RIGHT": Key.right,
}

SUPPORTED_KEYS = {
    "UP": Key.up,
    "DOWN": Key.down,
    "LEFT": Key.left,
    "RIGHT": Key.right,
    "SPACE": Key.space,
    "W": KeyCode.from_char('w'),
    "A": KeyCode.from_char('a'),
    "S": KeyCode.from_char('s'),
    "D": KeyCode.from_char('d'),
}
PREDEFINED_PARAMETERS = ['5', '10', '15']


SESSION_EXERCISES = [
        Exercise(name="Raising on toes", code="TT", instruction="Stand on your toes!",
                 reps=['5', '10', '15'],
                 ),
        Exercise(name="Toe Clenches", code="TC", instruction="Clench your toes like a fist!",
                 reps=['5', '10', '15'],
                 ),
        # Exercise(name="Standing on toes", code="TS", instruction="Stand on your toes!",
        #          reps=['5', '10', '15'],
        #          ),
]

PREDEFINED_EXERCISES = [
        Exercise(name="Raising on toes", code="TT", instruction="Stand on your toes!",
                 reps=['5', '10', '15'],
                 ),
        Exercise(name="Toe Clenches", code="TC", instruction="Clench your toes like a fist!",
                 reps=['5', '10', '15'],
                 ),
    # Exercise(name="Standing on toes", code="TC", instruction="Stand on your toes!",
    #          reps=['5', '10', '15'],
    #          assigned_key=("LEFT", KEYS["LEFT"])),
    Exercise(
        name="Rest",
        code="R",
        instruction="Rest your feet...",
        reps=['0'],
    ),
    # Exercise(name="Toes UP", code="UP", instruction="Move your toes up!",
    #          assigned_key=("RIGHT", KEYS["RIGHT"])),
]

