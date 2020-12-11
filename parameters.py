from math import sqrt
from misc import BLUE, RED


class ParameterError(Exception):
    """Used when a parameter is given that will cause the program to break later"""
    pass


class Parameters:
    """
    ---SIMULATION PARAMETERS---
    grid_width - width (and height) of the grid of people, must be multiple of sqrt(district_size)
    district_size - number of people contained in a district, must be perfect square
    num_swaps - number of swaps to perform before rerunning simulation (or exiting), None for run infinitely
    simulation_time - how long (seconds) to run before rerunning simulation (or exiting), None for run infinitely
    num_simulations - number of simulation repeats to run before quiting, per process, use None for keep rerunning

    ---APPLICATION/VISUAL PARAMETERS---
    width, height - size of the window in pixels
    num_districts - number of districts in total (calculated automatically)
    help_party, hinder_party - party to give help/hinder in the gerrymandering process
    line_width - district line width
    ms_between_draws - number of ms between drawing districts. Each draw, num_swaps_per_draw swaps are done
    num_swaps_per_draw - number of swaps done for every draw, which are done ms_between_draws ms apart
    """
    def __init__(self, grid_width=24, district_size=16, num_swaps=None,
                 simulation_time=None, num_simulations=None,
                 width=480, height=480, help_party=BLUE, hinder_party=RED,
                 line_width=3, ms_between_draws=1, num_swaps_per_draw=1):
        self.grid_width = grid_width
        self.district_size = district_size
        self.num_swaps = num_swaps
        self.simulation_time = simulation_time
        self.num_simulations = num_simulations

        self.width, self.height = width, height
        self.num_districts = (grid_width ** 2) / district_size
        self.help_party = help_party
        self.hinder_party = hinder_party
        self.line_width = line_width
        self.ms_between_draws = ms_between_draws
        self.num_swaps_per_draw = num_swaps_per_draw

        if not sqrt(district_size).is_integer():
            raise ParameterError('districts start as squares, district_size must be a perfect square')
        if not sqrt(self.num_districts).is_integer():
            raise ParameterError('districts must be able to fit into the grid without remainders')

    def __repr__(self):
        inside = []
        for i, (k, v) in enumerate(self.__dict__.items()):
            if k == 'num_districts':  # num_districts is calculated
                continue
            if i in (2, 4, 9):
                inside.append(f'{k}: {v},\n')
            elif i in (0, 3, 5, 10):
                inside.append(f'    {k}: {v}, ')
            else:
                inside.append(f'{k}: {v}, ')
        inside = ''.join(inside)
        return f'Parameters(\n{inside}\n)'
