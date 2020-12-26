from math import sqrt
from simulation import BLUE, RED


class Parameters:
    """
    ---SIMULATION PARAMETERS---
    grid_width - width (and height) of the grid of people, must be multiple of sqrt(district_size)
    district_size - number of people contained in a district, must be perfect square
    num_swaps - number of swaps to perform before rerunning simulation (or exiting), None for run infinitely
    simulation_time - how long (seconds) to run before rerunning simulation (or exiting), None for run infinitely
    num_simulations - number of simulation repeats to run before quiting, per process, use None for keep rerunning

    ---APPLICATION/VISUAL PARAMETERS---
    canvas_width, canvas_height - size of the canvas in pixels
    num_districts - number of districts in total (calculated automatically)
    help_party, hinder_party - party to give help/hinder in the gerrymandering process
    favor_tie - whether or not to try to make more tied districts
    line_width - district line width
    sleep_between_draws - number of ms between drawing districts. Each draw, num_swaps_per_draw swaps are done
    num_swaps_per_draw - number of swaps done for every draw, which are done repeatedly while running
    """
    def __repr__(self):
        inside = ', '.join(f'{k}={v}' for k, v in self.__dict__.items())
        return f'Parameters({inside})'

    def __init__(self, grid_width=24, district_size=16,
                 num_swaps=None, simulation_time=None, num_simulations=None,
                 canvas_width=480, canvas_height=480, help_party=BLUE, favor_tie=False,
                 line_width=3, sleep_between_draws=0, num_swaps_per_draw=1):
        self.grid_width = grid_width
        self.district_size = district_size
        self.num_swaps = num_swaps
        self.simulation_time = simulation_time
        self.num_simulations = num_simulations

        self.canvas_width, self.canvas_height = canvas_width, canvas_height
        self.num_districts = (grid_width ** 2) / district_size
        assert help_party is BLUE or help_party is RED
        self.help_party = help_party
        self.hinder_party = BLUE if help_party is RED else RED
        self.favor_tie = favor_tie
        self.line_width = line_width
        self.sleep_between_draws = sleep_between_draws
        self.num_swaps_per_draw = num_swaps_per_draw

        if not sqrt(district_size).is_integer():
            raise ValueError('districts start as squares, district_size must be a perfect square')
        if not sqrt(self.num_districts).is_integer():
            raise ValueError('districts must be able to fit into the grid without remainders')
