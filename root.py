import atexit
from canvas import Canvas
from misc import profile
from parameters import Parameters
import random
import tkinter as tk

"""
TODO:
- order conditions in getting people to swap for efficiency (think about how much it filters out to run less conditions)
- fix bug in harmful checks - if one party is switching from tie to red, and the other is switching from red to tie, it
  will say harmful, even though it is not harmful to the total score. This will allow tied districts to appear to move
- expand upon ideal_give_away
- safe import line_profiler
- why does it go slower when we have more swaps per draw
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

        if parameters.print_profiler:
            atexit.register(profile.print_stats)

        self.simulation_number = 1

        self.canvas = Canvas(self, parameters)

        self.geometry(f'{parameters.width}x{parameters.height}+1060+100')
        self.mainloop()
