from canvas import Canvas
from parameters import Parameters
import random
import tkinter as tk

"""
TODO:
-  - if one party is switching from tie to red, and the other is switching from red to tie, it
  will say harmful, even though it is not harmful to the total score. This will allow tied districts to appear to move
- change tests mostly back (probably keep simulation data) but add third stat that combines speed and score
- expand upon ideal_give_away
- fix imperfect touching p1 check if it would be disconnected (says it will when it wont)
- safe import line_profiler
- mess around with district1 order (maybe district2 order)
- make test more consistent
- change terminology for advantage/disadvantage
- why does it go slower when we have more swaps per draw
- reward for more than just flipping a district (margins? decide if district is competitive or all red?)
- record swaps already done, don't undo an already done swap
- prioritize keeping districts more cohesive?
- more profiling
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
        self.simulation_data_list = []

        self.canvas = Canvas(self, parameters)

        self.geometry(f'{parameters.width}x{parameters.height}+1060+100')
        self.mainloop()
