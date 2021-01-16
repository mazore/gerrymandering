from .hover_info import HoverInfo
from parameters import ParameterDocs
import tkinter as tk


class ParameterAdjusterBase:
    """The base class of parameter adjuster types (like Picker & Entry), and those are subclassed in picker_adjusters.py
    into adjusters of specific parameters (like DistrictSizeAdjuster & GridWidthAdjuster)"""

    def __init__(self, parameter_panel, name, pad_y=0, advanced=False, update_on_change=False):
        self.parameter_panel = parameter_panel
        self.name = name
        self.pad_y = pad_y
        self.advanced = advanced
        self.update_on_change = update_on_change

        self.var = tk.StringVar(value=str(getattr(parameter_panel.root.parameters, name)))
        self.var.trace('w', self.on_var_change)
        self.bold_font = self.parameter_panel.root.font + ' bold'

        self.frame = tk.Frame(parameter_panel)
        self.label = tk.Label(self.frame, text=name + ':')
        self.info = tk.Label(self.frame, text='ⓘ')
        HoverInfo(self.info, getattr(ParameterDocs, name))

        self.info.pack(side='left', padx=(0, 5))
        self.label.pack(side='left')
        if not advanced:
            self.pack()

    def pack(self):
        self.frame.pack(side='top', padx=(0, 5), pady=self.pad_y)

    def get(self):
        value = self.var.get()
        if value is None or value == 'invalid':
            return value
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
        font = self.bold_font if is_changed else self.parameter_panel.root.font
        self.label.config(font=font)

    def after_choice(self, choice):
        """Overridden by subclasses, called after the variable is changed. Typically used to ensure other entered
        parameters are valid"""
        pass
