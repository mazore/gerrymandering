from math import sqrt
from parties import *

"""
WIDTH, HEIGHT - size of the window
GRID_WIDTH - width (and height) of the grid of people, must be multiple of sqrt(DISTRICT_SIZE)
DISTRICT_SIZE - number of people contained in a district, must be perfect square
NUM_DISTRICTS - number of districts in total
ADVANTAGE, DISADVANTAGE - party to give advantage/disadvantage to in the gerrymandering process
LINE_WIDTH - district line width
NUM_SWAPS - number of swaps to perform before rerunning simulation (or exiting), use None for don't rerun
MS_BETWEEN_DRAWS - number of ms between drawing districts. Each draw of districts, NUM_SWAPS_PER_DRAW swaps are done
NUM_SWAPS_PER_DRAW - number of swaps done for every draw, which are done MS_BETWEEN_DRAWS ms apart

NUM_PROCESSES - the number of processes (windows) to run simultaneously using multiprocessing. Usually don't exceed 10
NUM_SIMULATIONS - number of simulation repeats to run before quiting (per process), use None for don't exit
OUTPUT_SCORES - whether or not to print the score of the advantaged party at the end of each simulation
OUTPUT_PROFILER - whether or not to print line_profiler results (use @profile from misc module) on window close
"""

WIDTH, HEIGHT = 480, 480
GRID_WIDTH = 24
DISTRICT_SIZE = 16
NUM_DISTRICTS = (GRID_WIDTH ** 2) / DISTRICT_SIZE
ADVANTAGE = BLUE
DISADVANTAGE = ADVANTAGE.opponent
LINE_WIDTH = 3
NUM_SWAPS = 1000
MS_BETWEEN_DRAWS: int = 1
NUM_SWAPS_PER_DRAW = 1

NUM_PROCESSES = 5
NUM_SIMULATIONS = 10
OUTPUT_SCORES = True
OUTPUT_PROFILER = False

if not sqrt(DISTRICT_SIZE).is_integer():
    raise ValueError('districts start as squares, DISTRICT_SIZE must be a perfect square')
if not sqrt(NUM_DISTRICTS).is_integer():
    raise ValueError('districts must be able to fit into the grid without remainders')
