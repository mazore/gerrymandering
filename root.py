from parameters import Parameters
import random
from simulation import Canvas
import tkinter as tk
from ui import *


class Root(tk.Tk):
    """Manages UI objects and Canvas, subclass of tkinter application root (represents a window)"""

    def __init__(self, parameters=Parameters(), seed=None, testing_parameter=None):
        self.parameters = parameters
        self.testing_parameter = testing_parameter
        super().__init__()
        self.font = 'Consolas 9'
        self.option_add('*font', self.font)

        if seed is not None:
            random.seed(seed)

        self.run_id = None
        self.simulation_datas = []
        self.simulation_number = 1

        self.canvas = Canvas(self)
        self.canvas.pack(side='right')
        # self.run_id = self.after(1, self.canvas.run)
        self.ui_frame = tk.Frame()
        self.ui_frame.pack(side='right', anchor='n')

        self.info_panel = InfoPanel(self)
        self.control_panel = ControlPanel(self)
        self.parameter_panel = ParameterPanel(self)

        self.info_panel.pack(side='top')
        self.control_panel.pack(side='top', pady=3)
        self.parameter_panel.pack(side='top')

        self.geometry('+100+100')
        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.mainloop()

    def on_close(self):
        self.canvas.pause()
        if self.run_id is not None:  # needed if not set in __init__
            self.after_cancel(self.run_id)
        self.after_cancel(self.info_panel.after_id)
        self.destroy()

    def reset_simulation(self):
        """Makes a new simulation by creating a new Canvas, and saves the current simulation data"""
        self.simulation_datas.append(self.canvas.get_simulation_data())

        was_running = self.canvas.running
        self.canvas.running = False
        if self.simulation_number == self.canvas.parameters.num_simulations:
            self.quit()
            return
        self.canvas.pack_forget()
        self.simulation_number += 1

        self.canvas = Canvas(self)
        self.canvas.pack(side='right')
        self.ui_frame.pack_forget()
        self.ui_frame.pack(side='right', anchor='n')
        if was_running:
            self.run_id = self.after(1, self.canvas.run)
