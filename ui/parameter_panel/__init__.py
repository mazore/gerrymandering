from .adjusters import all_adjusters
from .toggle_advanced_button import ToggleAdvancedButton
from parameters import Parameters
import tkinter as tk


class ParameterPanel(tk.Frame):
    """A box that contains parameter adjusters that are used to adjust simulation parameters"""

    def __init__(self, root):
        self.root = root
        self.parameters = root.parameters
        super().__init__(root.ui_frame, bd=1, relief='solid')

        adjuster_instances = (adjuster_type(self) for adjuster_type in all_adjusters)
        self.adjusters = {adjuster.name: adjuster for adjuster in adjuster_instances}

        self.toggle_advanced_button = ToggleAdvancedButton(self)

    def get_parameters(self):
        """Get a parameter object with all parameters set in this panel"""
        kwargs = {name: adjuster.get() for name, adjuster in self.adjusters.items()}
        if any(parameter == 'invalid' for parameter in kwargs.values()):
            return None
        return Parameters(**kwargs)

    def set_parameter(self, name, value):
        setattr(self.root.parameters, name, value)

    def on_restart(self):
        for adjuster in self.adjusters.values():
            adjuster.label.config(font=self.root.font)
