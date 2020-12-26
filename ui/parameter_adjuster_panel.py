"""The ParameterAdjusterPanel is a box that contains parameter_adjusters that are used to adjust different parameters"""
from .parameter_adjusters import ChoicePicker, LabeledAdjuster
import tkinter as tk


class ParameterAdjusterPanel(tk.Frame):
    def __init__(self, root, parameters):
        self.root = root
        self.parameters = parameters
        super().__init__(width=200, height=parameters.canvas_height - 100, bd=1, relief='solid')

        self.adjusters = [
            LabeledAdjuster(self, 'grid_width', ChoicePicker, ([1, 4, 5, 6, 7, 8, 9],)),
            LabeledAdjuster(self, 'grid_width', ChoicePicker, ([1, 4, 5, 6, 7, 8, 9],)),
            LabeledAdjuster(self, 'grid_width', ChoicePicker, ([1, 4, 5, 6, 7, 8, 9],)),
        ]

        for adjuster in self.adjusters:
            adjuster.pack(side='top')
