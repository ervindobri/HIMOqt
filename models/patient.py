class Patient:
    def __init__(self,
                 id,
                 name: str = None,
                 age: int = None,
                 parameters: dict = None
                 ):
        self.id = id
        self.name = name
        self.age = age
        self.parameters = parameters
