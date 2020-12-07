from math import sqrt
from parties import BLUE, RED


class ParameterError(Exception):
    """Used when a parameter is given that will cause the program to break later"""
    pass


class Parameters:
    """
    ---SIMULATION PARAMETERS---
    grid_width - width (and height) of the grid of people, must be multiple of sqrt(district_size)
    district_size - number of people contained in a district, must be perfect square
    num_swaps - number of swaps to perform before rerunning simulation (or exiting), use None for run infinitely

    ---APPLICATION/VISUAL PARAMETERS---
    width, height - size of the window in pixels
    num_districts - number of districts in total (calculated automatically)
    advantage, disadvantage - party to give advantage/disadvantage to in the gerrymandering process
    line_width - district line width
    ms_between_draws - number of ms between drawing districts. Each draw, num_swaps_per_draw swaps are done
    num_swaps_per_draw - number of swaps done for every draw, which are done ms_between_draws ms apart

    ---TESTING PARAMETERS---
    num_simulations - number of simulation repeats to run before quiting, per process, use None for keep rerunning
    score_list - multiprocessing.managers.ListProxy of scores of advantage at the end of the simulation. It is
      appended to at the end of each simulation
    print_profiler - whether or not to print results from line_profiler (misc.py) at the end of each process
    """
    def __init__(self, grid_width=24, district_size=16, num_swaps=None,
                 width=480, height=480, advantage=BLUE, disadvantage=RED,
                 line_width=3, ms_between_draws=1, num_swaps_per_draw=1,
                 num_simulations=None, score_list=None, print_profiler=False):
        self.grid_width = grid_width
        self.district_size = district_size
        self.num_swaps = num_swaps

        self.width, self.height = width, height
        self.num_districts = (grid_width ** 2) / district_size
        self.advantage = advantage
        self.disadvantage = disadvantage
        self.line_width = line_width
        self.ms_between_draws = ms_between_draws
        self.num_swaps_per_draw = num_swaps_per_draw

        self.num_simulations = num_simulations
        self.score_list = score_list
        self.print_profiler = print_profiler

        if not sqrt(district_size).is_integer():
            raise ParameterError('districts start as squares, district_size must be a perfect square')
        if not sqrt(self.num_districts).is_integer():
            raise ParameterError('districts must be able to fit into the grid without remainders')
