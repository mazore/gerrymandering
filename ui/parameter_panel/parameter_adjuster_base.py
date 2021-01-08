import tkinter as tk


class ParameterAdjusterBase:
    """The base class of parameter adjuster types (like Picker & Entry), and those are subclassed in picker_adjusters.py
    into adjusters of specific parameters (like DistrictSizeAdjuster & GridWidthAdjuster)"""

    def __init__(self, parameter_panel, name, var, pad_y=0, update_on_change=False):
        self.parameter_panel = parameter_panel
        self.name = name
        self.var = var
        self.var.trace('w', self.on_var_change)
        self.normal_font, self.bold_font = 'Consolas 9', 'Consolas 9 bold'
        self.update_on_change = update_on_change

        self.frame = tk.Frame(parameter_panel)
        self.label = tk.Label(self.frame, text=name + ':', font=self.normal_font)
        self.label.pack(side='left')
        self.frame.pack(side='top', pady=pad_y)

    def get(self):
        raw_value = self.var.get()
        if raw_value == 'none':
            return None
        try:
            return self.result_formatter(raw_value)
        except (ValueError, KeyError):
            return 'invalid'

    def set(self, value):
        self.var.set(value)

    def on_var_change(self, *_):
        value = self.get()
        if self.update_on_change:
            self.parameter_panel.set_parameter(self.name, value)
        else:
            self.update_boldness()
        self.after_choice(value)

    def update_boldness(self):
        changed = self.get() != getattr(self.parameter_panel.root.parameters, self.name)
        if changed:
            self.label.configure(font=self.bold_font)
        else:
            self.label.configure(font=self.normal_font)

    def after_choice(self, choice):
        """Overridden by subclasses, called after the variable is changed. Typically used to ensure other entered
        parameters are valid"""
        pass

    @staticmethod
    def result_formatter(value):
        """Overridden by subclasses, is called on the result of the widgets variable. Typically used to do typing or
        other conversions"""
        return value
