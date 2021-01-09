import tkinter as tk


class ParameterAdjusterBase:
    """The base class of parameter adjuster types (like Picker & Entry), and those are subclassed in picker_adjusters.py
    into adjusters of specific parameters (like DistrictSizeAdjuster & GridWidthAdjuster)"""

    def __init__(self, parameter_panel, name, pad_y=0, update_on_change=False):
        self.parameter_panel = parameter_panel
        self.name = name
        self.var = tk.StringVar(value=str(getattr(parameter_panel.root.parameters, name)))
        self.var.trace('w', self.on_var_change)
        self.normal_font, self.bold_font = 'Consolas 9', 'Consolas 9 bold'
        self.update_on_change = update_on_change

        self.frame = tk.Frame(parameter_panel)
        self.label = tk.Label(self.frame, text=name + ':', font=self.normal_font)
        self.label.pack(side='left')
        self.frame.pack(side='top', pady=pad_y)

    def get(self):
        value = self.var.get()
        if value in ('None', 'invalid'):
            return None
        return self.get_obj_from_str(value)

    def set(self, value):
        self.var.set(value)

    def get_obj_from_str(self, s):
        """self.var is always a string, so if it represents another, subclasses can convert it to the actual object
        here"""
        return s

    def on_var_change(self, *_):
        value = self.get()
        if self.update_on_change:
            self.parameter_panel.set_parameter(self.name, value)
        else:
            self.update_boldness()
        self.after_choice(value)

    def update_boldness(self):
        is_changed = self.get() != getattr(self.parameter_panel.root.parameters, self.name)
        if is_changed:
            self.label.configure(font=self.bold_font)
        else:
            self.label.configure(font=self.normal_font)

    def after_choice(self, choice):
        """Overridden by subclasses, called after the variable is changed. Typically used to ensure other entered
        parameters are valid"""
        pass
