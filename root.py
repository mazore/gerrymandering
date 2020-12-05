from canvas import Canvas
from parameters import Parameters
import random
import tkinter as tk

"""
TODO:
- use backtracking to pick swap districts/people, and use 6x6 example to test it. Use ideal_give_away, ideal_take_in,
  possible_take_in methods on district class. Order district 1's by their net_advantage.
- safe import line_profiler
- reward for more than just flipping a district (margins? decide if district is competitive or all red?)
- recursion error when no possible moves (mostly small grids)
- record swaps already done, don't undo an already done swap
- prioritize keeping districts more cohesive
- more profiling
- learn C and convert some code
- make settings class
- packages
- UI
- better documentation (readme)
- line smoothing (spline, make districts look more organic)
- multiple parties? make red and blue into other non american colors?
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
