class SimulationData:
    def __init__(self, score, num_swaps, total_time, total_swap_time):
        self.score = score
        self.num_swaps = num_swaps
        self.total_time = total_time
        self.total_swap_time = total_swap_time


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
TIE = Party('tie', '#000000')
