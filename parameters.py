from math import sqrt
from simulation import BLUE, RED


class ParameterDocs:
    help_party = 'Party to give help to in the gerrymandering process'
    favor_tie = 'Whether or not to try to make more tied districts'
    district_size = 'Number of people contained in a district, must be perfect square'
    grid_width = 'Width (and height) of the grid of people, must be multiple of sqrt(district_size)'
    num_swaps = 'Number of swaps to perform before rerunning simulation (or exiting), disabled for run infinitely'
    simulation_time = 'How long (seconds) to run before rerunning simulation (or exiting), disabled for run infinitely'
    canvas_width = 'Width (and height) of the canvas in pixels'
    line_width = 'District line width'
    sleep_between_draws = 'Number of ms between drawing districts. Each draw, num_swaps_per_draw swaps are done'
    num_swaps_per_draw = 'Number of swaps done for every draw, which are done repeatedly while running. Increase to ' \
                         'make faster but more chunky'
    # Hidden & convenience parameters
    hinder_party = 'Party to hinder in the gerrymandering process'
    num_simulations = 'Number of simulation repeats to run before quiting, per process, use None for keep rerunning'
    num_districts = 'Number of districts in total (calculated automatically)'


class Parameters:
    def __init__(self, num_simulations=None,
                 help_party=BLUE, favor_tie=False,
                 district_size=16, grid_width=24,
                 num_swaps=None, simulation_time=None,
                 canvas_width=480, line_width=3,
                 sleep_between_draws=0, num_swaps_per_draw=1):
        assert help_party in (BLUE, RED)
        self.help_party = help_party
        self.favor_tie = favor_tie
        self.district_size = district_size
        self.grid_width = grid_width
        self.num_swaps = num_swaps
        self.simulation_time = simulation_time
        self.canvas_width = canvas_width
        self.line_width = line_width
        self.sleep_between_draws = sleep_between_draws
        self.num_swaps_per_draw = num_swaps_per_draw
        # Hidden & convenience parameters
        self.hinder_party = BLUE if help_party == RED else RED
        self.num_simulations = num_simulations
        self.num_districts = (grid_width ** 2) / district_size

        if not sqrt(district_size).is_integer():
            raise ValueError('districts start as squares, district_size must be a perfect square')
        if not sqrt(self.num_districts).is_integer():
            raise ValueError('districts must be able to fit into the grid without remainders')

    def __repr__(self):
        inside = ', '.join(f'{k}={v}' for k, v in self.__dict__.items())
        return f'Parameters({inside})'
