from constants import *
from district import District
from math import ceil, sqrt
from parties import BLUE, RED, TIE
from person import Person
from random import random
from swap_manager import SwapManager
import tkinter as tk


class Canvas(tk.Canvas):
    """Manages people, districts, and swapping, subclass of tkinter Canvas"""

    def __init__(self, root):
        self.root = root
        super().__init__(width=WIDTH, height=HEIGHT)
        self.pack()

        self.running = False
        self.score = {BLUE: 0, RED: 0, TIE: 0}
        self.swap_manager = SwapManager(self)

        self.line_id_state_map = {}
        self.people_grid = []
        self.generate_people()

        self.districts = []
        self.generate_districts()

        self.run()

        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-2>', self.middle_click)
        self.bind('<Button-3>', self.right_click)

    def run(self):
        self.running = True
        self.swap_dispatch()

    def pause(self):
        self.running = False

    def rerun_simulation(self):
        if self.root.simulation_number == NUM_SIMULATIONS:
            quit()
        self.running = False
        self.pack_forget()
        self.root.simulation_number += 1
        self.root.canvas = Canvas(self.root)

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

        if NUM_SWAPS_PER_DRAW == 1:
            self.swap_manager.do_swap()
        else:  # if multiple swaps per draw
            to_draw = set()
            for _ in range(NUM_SWAPS_PER_DRAW):
                self.swap_manager.do_swap()
                to_draw.add(self.swap_manager.district1)
                to_draw.add(self.swap_manager.district2)
            for district in to_draw:
                district.draw()

        self.root.after(MS_BETWEEN_DRAWS, self.swap_dispatch)

    def generate_people(self):
        """Create grid of people with randomized parties"""
        # make sure people's parties are random but same number of people for each
        parties = [RED, BLUE] * ceil(GRID_WIDTH ** 2 / 2)
        parties = sorted(parties, key=lambda _: random())  # more efficient than random.shuffle

        party_num_people_map = {BLUE: 0, RED: 0, TIE: 0}
        square_width = WIDTH / GRID_WIDTH
        for y in range(0, GRID_WIDTH):
            row = []
            for x in range(0, GRID_WIDTH):
                person1 = (x * square_width, y * square_width)
                person2 = ((x + 1) * square_width, (y + 1) * square_width)
                party = parties[x + y * GRID_WIDTH]
                party_num_people_map[party] += 1
                row.append(Person(self, person1, person2, x, y, party=party))
            self.people_grid.append(row)
        for row in self.people_grid:
            for person in row:
                person.secondary_init()
        # print('people:', party_num_people_map)

    def generate_districts(self):
        """Generate square districts, of size DISTRICT_SIZE.

        We know this can fit because of assertions in constants.py"""
        district_width = sqrt(DISTRICT_SIZE)
        for grid_x in range(int(sqrt(NUM_DISTRICTS))):
            for grid_y in range(int(sqrt(NUM_DISTRICTS))):
                grid_person1 = grid_x * district_width, grid_y * district_width
                grid_person2 = (grid_x + 1) * district_width, (grid_y + 1) * district_width
                self.districts.append(District(self, grid_person1, grid_person2))
                self.score[self.districts[-1].winner] += 1
        # print('districts:', self.score)
