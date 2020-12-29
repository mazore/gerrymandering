import tkinter as tk


class ParameterAdjusterBase:
    """The base class of parameter adjuster types (like ChoicePicker & TextField), and those are subclassed in
    adjusters.py into adjusters of specific parameters (like DistrictSizeAdjuster & GridWidthAdjuster)"""

    def __init__(self, parameter_panel, name, var):
        self.parameter_panel = parameter_panel
        self.name = name
        self.var = var
        self.normal_font, self.bold_font = 'Consolas 9', 'Consolas 9 bold'

        self.frame = tk.Frame(parameter_panel)
        self.label = tk.Label(self.frame, text=name + ':', font=self.normal_font)
        self.label.pack(side='left')
        self.frame.pack(side='top')

    def get(self):
        value = self.var.get()
        if value == 'invalid':
            return None
        return self.result_formatter(value)

    def set(self, value):
        self.var.set(value)

    def update_boldness(self):
        changed = self.get() != getattr(self.parameter_panel.root.parameters, self.name)
        if changed:
            self.label.configure(font=self.bold_font)
        else:
            self.label.configure(font=self.normal_font)

    @staticmethod
    def result_formatter(value):
        """Overridden by subclasses, is called on the result of the widgets variable. Typically used to do typing or
        other conversions"""
        return value
