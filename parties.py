class Party:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Blue(Party):
    def __init__(self):
        super().__init__('blue', '#5868aa')

    @property
    def opponent(self):
        return RED


class Red(Party):
    def __init__(self):
        super().__init__('red', '#f95955')

    @property
    def opponent(self):
        return BLUE


class Tie(Party):
    def __init__(self):
        super().__init__('tie', 'black')


BLUE = Blue()
RED = Red()
TIE = Tie()
