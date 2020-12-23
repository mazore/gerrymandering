from canvas import Canvas
from parameters import Parameters
import random
import tkinter as tk

"""
TODO:
- make it possible to have TIE be help_party
- readme roadmap & contribution section
- add a "most recent stats" file
- more profiling
- packages
- UI
- implement get_district2_weight in District class
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

        self.run_id = None
        self.simulation_datas = []
        self.simulation_number = 1

        self.canvas = Canvas(self, parameters)
        self.run_id = self.after(1, self.canvas.run)

        self.geometry(f'{parameters.width}x{parameters.height}+1060+100')
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.mainloop()

    def on_close(self):
        self.canvas.running = False
        if self.run_id is not None:
            self.after_cancel(self.run_id)
        self.destroy()

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
        self.run_id = self.after(1, self.canvas.run)
