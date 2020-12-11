from canvas import Canvas
from parameters import Parameters
import random
from misc import SimulationData
import tkinter as tk

"""
TODO:
- break down get_people into 2 or 4 methods
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
        self.parameters = parameters
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
        self.simulation_datas.append(SimulationData(
            self.canvas.get_score()[self.parameters.advantage.name],
            self.canvas.swap_manager.swaps_done,
            self.canvas.total_swap_time
        ))

        self.canvas.running = False
        if self.simulation_number == self.parameters.num_simulations:
            self.quit()
            return
        self.canvas.pack_forget()
        self.simulation_number += 1
        self.canvas = Canvas(self, self.parameters)
