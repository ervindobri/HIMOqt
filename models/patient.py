class Patient:
    def __init__(self,
                 id,
                 name: str = None,
                 age: int = None,
                 parameters=None
                 ):
        self.id = id
        self.name = name
        self.age = age
        self.parameters = parameters

    def __str__(self) -> str:
        return "Id" + str(self.id) + ", Name:" + self.name + ", Age:" + str(self.age) + ", Parameters:" + str(self.parameters)


