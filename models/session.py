from helpers.constants import PREDEFINED_EXERCISES, SESSION_EXERCISES, STANDING


class Session:
    def __init__(self, reps=0, pause=0):
        self.reps = reps
        self.pause = pause
        self.exercises = SESSION_EXERCISES

        # hanyat csinalt meg minden gyakorlatbol
        self.counterMap = self.setupMap()
        self.pause_active = False
        self.current_exercise_name = self.exercises[0].name
        self.next_exercise_name = self.exercises[1].name
        print("Session - reps: ", self.reps, ", pause: ", self.pause)

        # self.is_last = False
        self.total_exercises = len(self.exercises)
        self.done = 0
        # flow: ex -> pause -> ex -> pause -> standing on toes
        self.standing_on_toes_secs = 0
        self.standing_reps = int(self.pause)*2
        self.session_finished = False

    def setupMap(self):
        counterMap = {}
        codes = [x.code for x in self.exercises]
        for code in codes:
            counterMap[code] = 0
        return counterMap

    def get_code(self, exercise):
        code = next((x.code for x in self.exercises if x.name == exercise), None)
        return code

    def all_done(self):
        if self.done == self.total_exercises:
            return True
        return False

    def increment(self, exercise):
        print(exercise)
        if not self.all_done():
            code = self.get_code(exercise)
            if exercise == self.current_exercise_name and not self.pause_active:

                # If exercise is not completed, increment value in dict and 'correct'
                if not self.is_completed(exercise):
                    self.counterMap[code] += 1
                    return True
                else:
                    # If its complete -> pause for 10..20..30 secs -> next exercise and INCREMENT
                    self.counterMap[code] += 1
                    # set current and next
                    self.current_exercise_name = self.next_exercise_name
                    self.next_exercise_name = self.get_next(code)
                    self.pause_active = True
                    return True
            return False
        else:
            if self.standing_on_toes_secs < self.standing_reps:
                self.current_exercise_name = STANDING
            else:
                self.session_finished = True
            return True if exercise == STANDING else False

    # Check if current exercise reps are equal to total reps
    def is_completed(self, exercise):
        code = self.get_code(exercise)
        return True if self.counterMap[code] == int(self.reps)-1 else False

    # Get the name of the next exercise
    def get_next(self, code):
        res = None
        temp = iter(self.counterMap)
        for key in temp:
            if key == code:
                res = next(temp, None)

        name = next((x.name for x in self.exercises if x.code == res), "NO NEXT")
        return name

    # Get current reps: done/total
    def current_status(self):
        if self.pause_active:
            return "Pause"
        else:
            code = self.get_code(self.current_exercise_name)
            return str(self.counterMap[code]) + '/' + str(self.reps)
