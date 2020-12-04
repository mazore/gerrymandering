from canvas import Canvas
from parameters import Parameters
import random
import tkinter as tk

"""
TODO:
- make a district use its net_advantage to determine what type of person it wants to get rid of/take in
- reward for more than just flipping a district (margins? decide if district is competitive or all red?)
- recursion error when no possible moves (mostly small grids)
- record swaps already done, don't undo an already done swap
- prioritize keeping districts more cohesive
- more profiling
- make settings class
- packages
- UI
- better documentation (readme)
- line smoothing (spline, make districts look more organic)
- multiple parties?
"""


class Root(tk.Tk):
    """Manages UI things, subclass of tkinter application root (represents a window)"""

    def __init__(self, parameters=Parameters(), seed=None):
        super().__init__()

        if seed is not None:
            random.seed(seed)

        self.simulation_number = 1

        self.canvas = Canvas(self, parameters)

        self.geometry(f'{parameters.width}x{parameters.height}+1060+100')
        self.mainloop()
