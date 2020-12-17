from canvas import Canvas
from parameters import Parameters
import random
import tkinter as tk

"""
TODO:
- reward for more than just flipping a district (margins? decide if district is competitive or all red?)
- record swaps already done, don't undo an already done swap
- prioritize keeping districts more cohesive?
- implement get_district2_weight
- more profiling
- packages
- UI
- readme
- better performance by different drawing method (not tkinter.Canvas), maybe website (flask)
- line smoothing (spline, make districts look more organic)
- multiple parties? make red and blue into other non american colors?
"""


class Root(tk.Tk):
    """Manages UI things, subclass of tkinter application root (represents a window)"""

    def __init__(self, parameters=Parameters(), seed=None, testing_parameter=None):
        self.parameters = parameters
        self.testing_parameter = testing_parameter

        super().__init__()

        if seed is not None:
            random.seed(seed)

        self.simulation_datas = []
        self.simulation_number = 1

        self.canvas = Canvas(self, parameters)

        self.geometry(f'{parameters.width}x{parameters.height}+1060+100')
        self.mainloop()

    def rerun_simulation(self):
        """Makes a new simulation by creating a new Canvas, and saves the current simulation data"""
        self.simulation_datas.append(self.canvas.get_simulation_data())

        self.canvas.running = False
        if self.simulation_number == self.parameters.num_simulations:
            self.quit()
            return
        self.canvas.pack_forget()
        self.simulation_number += 1
        self.canvas = Canvas(self, self.parameters)
