from parameters import Parameters
import random
from simulation import Canvas
import tkinter as tk
from ui import ControlPanel, ParameterPanel


class Root(tk.Tk):
    """Manages UI objects and Canvas, subclass of tkinter application root (represents a window)"""

    def __init__(self, parameters=Parameters(), seed=None, testing_parameter=None):
        self.parameters = parameters
        self.testing_parameter = testing_parameter
        super().__init__()

        if seed is not None:
            random.seed(seed)

        self.run_id = None
        self.simulation_datas = []
        self.simulation_number = 1

        self.canvas = Canvas(self)
        self.control_panel = ControlPanel(self)
        self.parameter_panel = ParameterPanel(self)
        self.canvas.grid(column=1, row=1)
        self.control_panel.grid(column=2, row=1, sticky='s', pady=5)
        self.parameter_panel.grid(column=2, row=1)

        self.run_id = self.after(1, self.canvas.run)

        self.geometry('+100+100')
        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.mainloop()

    def on_close(self):
        self.canvas.pause()
        if self.run_id is not None:
            self.after_cancel(self.run_id)
        self.destroy()

    def rerun_simulation(self):
        """Makes a new simulation by creating a new Canvas, and saves the current simulation data"""
        self.simulation_datas.append(self.canvas.get_simulation_data())

        was_running = self.canvas.running
        self.canvas.running = False
        if self.simulation_number == self.canvas.parameters.num_simulations:
            self.quit()
            return
        self.canvas.grid_remove()
        self.simulation_number += 1

        self.canvas = Canvas(self)
        self.canvas.grid(column=1, row=1)
        if was_running:
            self.run_id = self.after(1, self.canvas.run)
