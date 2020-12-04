class Party:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


BLUE = Party('blue', '#5868aa')
RED = Party('red', '#f95955')
TIE = Party('tie', 'black')
