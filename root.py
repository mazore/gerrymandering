from canvas import Canvas
from constants import WIDTH, HEIGHT
import tkinter as tk

"""
TODO:
- prioritize swapping districts (and people) with different parties
- change constants.py to parameters.py (reformat documentation)
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

    def __init__(self, _=None):
        super().__init__()

        self.simulation_number = 1

        self.canvas = Canvas(self)

        self.geometry(f'{WIDTH}x{HEIGHT}+1060+100')
        self.mainloop()
