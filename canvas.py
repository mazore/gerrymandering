from district import District
from math import ceil, sqrt
from misc import fast_shuffled
from parties import BLUE, RED
from person import Person
from misc import SimulationData
from swap_manager import SwapManager
import tkinter as tk
from time import time


class Canvas(tk.Canvas):
    """Manages people, districts, and swapping, subclass of tkinter Canvas"""

    def __init__(self, root, parameters):
        self.root = root
        self.parameters = parameters
        super().__init__(width=parameters.width, height=parameters.height)
        self.pack()

        self.running = False
        self.swap_manager = SwapManager(self)

        self.line_id_state_map = {}  # {tkinter.Canvas id for the line: the current state ('hidden' or 'normal')}
        self.people_grid = []
        self.generate_people()

        self.districts = []
        self.generate_districts()

        self.start_time = time()
        self.root.after(1, self.run)

        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-2>', self.middle_click)
        self.bind('<Button-3>', self.right_click)

    def run(self):
        if not self.running:
            self.running = True
            self.swap_dispatch()

    def pause(self):
        self.running = False

    def rerun_simulation(self):
        self.root.simulation_data_list.append(SimulationData(
            self.get_score()[self.parameters.advantage.name],
            self.swap_manager.swaps_done,
            time() - self.start_time
        ))

        self.running = False
        if self.root.simulation_number == self.parameters.num_simulations:
            self.root.quit()
            return
        self.pack_forget()
        self.root.simulation_number += 1
        self.root.canvas = Canvas(self.root, self.parameters)

    def left_click(self, _):
        self.run()

    def middle_click(self, _):
        if not self.districts:  # if no districts
            self.generate_districts()

    def right_click(self, _):
        self.pause()

    def swap_dispatch(self):
        if not self.running:
            return

        self.swap_manager.swap_dispatch()

        self.root.after(self.parameters.ms_between_draws, self.swap_dispatch)

    def get_score(self):
        """Return a dict of format {party_name: num_districts_won, ...}"""
        score = {'blue': 0, 'red': 0, 'tie': 0}
        for district in self.districts:
            score[district.get_winner().name] += 1
        return score

    def generate_people(self):
        """Create grid of people with randomized parties"""
        # make sure peoples parties are random but same number of people for each
        parties = [RED, BLUE] * ceil(self.parameters.grid_width ** 2 / 2)
        parties = fast_shuffled(parties)

        square_width = self.parameters.width / self.parameters.grid_width
        for grid_y in range(0, self.parameters.grid_width):
            row = []
            for grid_x in range(0, self.parameters.grid_width):
                p1 = (grid_x * square_width, grid_y * square_width)
                p2 = ((grid_x + 1) * square_width, (grid_y + 1) * square_width)
                party = parties[grid_x + grid_y * self.parameters.grid_width]
                row.append(Person(self, p1, p2, grid_x, grid_y, party=party))
            self.people_grid.append(row)
        for row in self.people_grid:
            for person in row:
                person.secondary_init()

    def generate_districts(self):
        """Generate square districts, of size district_size.

        We know this can fit because of assertions in constants.py
        """
        district_width = sqrt(self.parameters.district_size)
        for grid_x in range(int(sqrt(self.parameters.num_districts))):
            for grid_y in range(int(sqrt(self.parameters.num_districts))):
                grid_p1 = grid_x * district_width, grid_y * district_width
                grid_p2 = (grid_x + 1) * district_width, (grid_y + 1) * district_width
                self.districts.append(District(self, grid_p1, grid_p2))
