import tkinter as tk


class ParameterAdjusterBase:
    """The base class of parameter adjuster types (like ChoicePicker & TextField), and those are subclassed in
    adjusters.py into adjusters of specific parameters (like DistrictSizeAdjuster & GridWidthAdjuster)"""

    def __init__(self, parameter_panel, name, var):
        self.parameter_panel = parameter_panel
        self.name = name
        self.var = var

        self.frame = tk.Frame(parameter_panel)
        tk.Label(self.frame, text=name + ':').pack(side='left')
        self.frame.pack(side='top')

    def get(self):
        value = self.var.get()
        if value == 'invalid':
            return None
        return self.result_formatter(value)

    def set(self, value):
        self.var.set(value)

    @staticmethod
    def result_formatter(value):
        """Overridden by subclasses, is called on the result of the widgets variable. Typically used to do typing or
        other conversions"""
        return value
