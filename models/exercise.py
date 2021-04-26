from pynput.keyboard import Key, KeyCode


class Exercise:
    def __init__(self,
                 name: str = "Exercise",
                 code: str = "EX",  # abbreviation of exercise name
                 instruction: str = "Do this, do that!",
                 reps: list = None,
                 ):
        self.name = name
        self.code = code
        self.reps = reps
        self.instruction = instruction

    def serialize(self):
        return {
            "name": self.name,
            "code": self.code,
            "instruction": self.instruction,
        }
