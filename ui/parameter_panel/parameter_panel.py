from .adjusters import *
from parameters import Parameters
import tkinter as tk


class ParameterPanel(tk.Frame):
    """A box that contains parameter adjusters that are used to adjust simulation parameters"""

    def __init__(self, root):
        self.root = root
        self.parameters = root.parameters
        super().__init__(width=200, height=root.parameters.canvas_height - 100, bd=1, relief='solid')

        adjusters = [DistrictSizeAdjuster(self), GridWidthAdjuster(self), HelpPartyAdjuster(self)]
        self.adjusters = {adjuster.name: adjuster for adjuster in adjusters}

    def get_parameters(self):
        """Get a parameter object with all parameters set in this panel"""
        kwargs = {name: self.get_parameter(name) for name in self.adjusters.keys()}
        if any(parameter is None for parameter in kwargs.values()):
            return None
        return Parameters(**kwargs)

    def get_parameter(self, name):
        """Returns the parameter by name, as set in this panel"""
        return self.adjusters[name].get()

    def on_rerun(self):
        for adjuster in self.adjusters.values():
            adjuster.label.configure(font=adjuster.normal_font)
