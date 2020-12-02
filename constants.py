from math import sqrt
from parties import *

# size of the window
WIDTH, HEIGHT = 480, 480
# width (and height) of the grid of people
GRID_WIDTH = 24  # 48
# number of people contained in a district
DISTRICT_SIZE = 16  # 36
# number of districts in total
NUM_DISTRICTS = (GRID_WIDTH ** 2) / DISTRICT_SIZE
# party to give advantage to in the gerrymandering process
ADVANTAGE = BLUE
# party to disadvantage in the gerrymandering to process
DISADVANTAGE = ADVANTAGE.opponent
# district line width
LINE_WIDTH = 3
# number of swaps to perform before rerunning simulation (or exiting), use None for don't rerun
NUM_SWAPS = 1000
# number of ms between drawing districts, each draw of districts NUM_SWAPS_PER_DRAW swaps are done, minimum 1
MS_BETWEEN_DRAWS: int = 1  # 1000
# number of swaps of people between districts, for every draw which are done MS_BETWEEN_DRAWS ms apart.
NUM_SWAPS_PER_DRAW = 1
# the number of processes (windows) to run simultaneously using multiprocessing. Usually don't exceed 10
NUM_PROCESSES = 5
# number of simulation repeats to run before quiting (per process) use None for don't exit, 1 for don't repeat
NUM_SIMULATIONS = 10
# whether or not to print the score of the advantaged party at the end of each simulation
OUTPUT_SCORES = True

# districts are squares, DISTRICT_SIZE must be a perfect square
assert sqrt(DISTRICT_SIZE).is_integer()
# this ensures districts are able to fit into the grid without remainders
assert sqrt(NUM_DISTRICTS).is_integer()
