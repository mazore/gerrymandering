from .district import District
from .draw_modes import DrawModeManager
from .misc import BLUE, RED, SimulationData
from .person import Person
from .swap_manager import SwapManager
from math import ceil, sqrt
from misc import fast_shuffled
import tkinter as tk
from time import sleep, time


class Canvas(tk.Canvas):
    """Manages people, districts, and swapping, subclass of tkinter Canvas"""

    def __init__(self, root):
        self.root = root
        self.parameters = root.parameters
        super().__init__(width=root.parameters.canvas_width, height=root.parameters.canvas_width)

        self.draw_mode_manager = DrawModeManager(self)
        self.running = False
        self.swap_manager = SwapManager(self)

        self.line_id_state_map = {}  # {tkinter.Canvas id for the line: current state ('hidden' or 'normal')}
        self.people_grid = []  # 2d list of Person objects
        self.generate_people()

        self.show_districts = True
        self.districts = []
        self.generate_districts()

        self.start_time = time()
        self.total_swap_time = 0  # Total time spent in the swap_manager.swap function in seconds

        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-2>', self.middle_click)
        self.bind('<Button-3>', self.right_click)

    def run(self):
        """Start running or resume from being paused and update play_pause button"""
        self.running = True
        self.root.control_panel.play_pause_button.update_config()
        while True:
            if not self.running:
                break
            self.swap_manager.swap_dispatch()
            self.root.update()
            if self.parameters.sleep_between_draws != 0:
                sleep(self.parameters.sleep_between_draws / 1000)

    def pause(self):
        """Stop the simulation from doing swaps and update play_pause button"""
        self.running = False
        self.root.control_panel.play_pause_button.update_config()

    def left_click(self, _):
        self.root.control_panel.play_pause_button.play_pause()

    def middle_click(self, _):
        # self.toggle_districts_visible()
        self.root.control_panel.restarting_button.restart()

    def right_click(self, _):
        if not self.running:
            self.swap_manager.swap_dispatch()
            self.root.update()

    def toggle_districts_visible(self):
        self.pause()
        state = 'hidden' if self.show_districts else 'normal'
        for person in self.iter_people():
            self.itemconfig(person.outer_id, state=state)
        self.show_districts = not self.show_districts
        [district.draw() for district in self.districts]
        self.root.control_panel.toggle_districts_button.update_config()

    def get_simulation_data(self):
        return SimulationData(
            self.get_score()['tie' if self.parameters.favor_tie else self.parameters.help_party.name],
            self.swap_manager.swaps_done,
            time() - self.start_time,
            self.total_swap_time
        )

    def get_score(self):
        """Return a dict of format {party_name: num_districts_won, ...}"""
        score = {'blue': 0, 'red': 0, 'tie': 0}
        for district in self.districts:
            score[district.get_winner().name] += 1
        return score

    def iter_people(self):
        for row in self.people_grid:
            for person in row:
                yield person

    def generate_people(self):
        """Create grid of people with randomized parties"""
        # Make sure peoples parties are random but same number of people for each
        parties = [RED, BLUE] * ceil(self.parameters.grid_width ** 2 / 2)
        parties = fast_shuffled(parties)

        square_width = self.parameters.canvas_width / self.parameters.grid_width
        for grid_y in range(0, self.parameters.grid_width):
            row = []
            for grid_x in range(0, self.parameters.grid_width):
                p1 = (grid_x * square_width, grid_y * square_width)
                p2 = ((grid_x + 1) * square_width, (grid_y + 1) * square_width)
                party = parties[grid_x + grid_y * self.parameters.grid_width]
                row.append(Person(self, p1, p2, grid_x, grid_y, party=party))
            self.people_grid.append(row)
        for person in self.iter_people():
            person.secondary_init()

    def generate_districts(self):
        """Generate square districts of size district_size. We know this can fit because of assertions in Parameters
        initialization"""
        district_width = sqrt(self.parameters.district_size)
        for grid_x in range(int(sqrt(self.parameters.num_districts))):
            for grid_y in range(int(sqrt(self.parameters.num_districts))):
                grid_p1 = grid_x * district_width, grid_y * district_width
                grid_p2 = (grid_x + 1) * district_width, (grid_y + 1) * district_width
                self.districts.append(District(self, grid_p1, grid_p2))
