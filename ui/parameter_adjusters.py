from .adjuster_container import AdjusterContainer
from .adjuster_types import ChoicePicker
from math import sqrt
import tkinter as tk


class ParameterAdjusters(tk.Frame):
    """A box that contains adjuster_types that are used to adjust simulation parameters"""
    def __init__(self, root, parameters):
        self.root = root
        self.parameters = parameters
        super().__init__(width=200, height=parameters.canvas_height - 100, bd=1, relief='solid')

        self.adjuster_containers = [
            AdjusterContainer(self, ChoicePicker, 'district_size', 16, get_choices=self.get_district_size_choices),
            AdjusterContainer(self, ChoicePicker, 'grid_width', 24, get_choices=self.get_grid_width_choices),
        ]
        self.adjusters = {ac.name: ac.adjuster for ac in self.adjuster_containers}

    def get_parameter(self, name):
        """Returns the parameter by name as set in this frame"""
        return self.adjusters[name].var.get()

    @staticmethod
    def get_district_size_choices():
        return [i*i for i in range(2, 10)]

    def get_grid_width_choices(self):
        district_width = int(sqrt(int(self.get_parameter('district_size'))))
        return [districts_per_row * district_width for districts_per_row in range(2, 15)]
