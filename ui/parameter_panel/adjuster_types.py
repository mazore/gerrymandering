from .parameter_adjuster_base import ParameterAdjusterBase
from math import inf
import tkinter as tk


class CheckboxAdjusterType(ParameterAdjusterBase):
    """Can be used to toggle a boolean on or off"""

    def __init__(self, parameter_panel, name, **kwargs):
        super().__init__(parameter_panel, name, pad_y=3, **kwargs)

        self.widget = tk.Checkbutton(self.frame, variable=self.var)
        self.widget.pack(side='left')

    def get_obj_from_str(self, s):
        if s in ('0', 'False'):
            return False
        if s in ('1', 'True'):
            return True
        raise ValueError


class EntryAdjusterType(ParameterAdjusterBase):
    """Can be used to enter a value into a field"""

    def __init__(self, parameter_panel, name, type_,
                 width=5, use_checkbutton=False, disabled_value=None, min_=None, max_=None, **kwargs):
        self.type = type_
        self.min, self.max = min_, max_
        """min, max - both inclusive, range of values before becoming invalid"""
        self.min = -inf if self.min is None else self.min
        self.max = inf if self.max is None else self.max
        super().__init__(parameter_panel, name, pad_y=5, **kwargs)

        self.widget = tk.Entry(self.frame, textvariable=self.var, width=width, relief='solid')
        self.widget.bind('<Return>', lambda _: self.parameter_panel.root.focus())

        self.use_checkbutton = use_checkbutton
        if use_checkbutton:
            self.checkbutton_var = tk.BooleanVar(value=self.var.get() != 'None')
            self.checkbutton_var.trace('w', self.update_disabled)
            self.checkbutton = tk.Checkbutton(self.frame, variable=self.checkbutton_var)
            self.checkbutton.pack(side='left')
            if self.var.get() == 'None':
                self.var.set(disabled_value)
            self.update_disabled()

        self.widget.pack(side='left')

    def get_obj_from_str(self, s):
        if self.use_checkbutton and not self.checkbutton_var.get():
            return None
        try:
            result = self.type(s)
            if self.min <= result <= self.max:
                return result
            return 'invalid'
        except ValueError:
            return 'invalid'

    def update_disabled(self, *_):
        if self.checkbutton_var.get():
            self.widget.config(relief='solid', state='normal')
        else:
            self.widget.config(relief='sunken', state='disabled')
        self.update_boldness()


class PickerAdjusterType(ParameterAdjusterBase):
    """Can be used to choose an item from a list of (or function that returns) choices, shown as a dropdown list"""

    def __init__(self, parameter_panel, name, **kwargs):
        super().__init__(parameter_panel, name, **kwargs)

        self.widget = tk.OptionMenu(self.frame, self.var, None)
        self.widget.bind('<Button-1>', self.on_dropdown)
        self.widget.pack(side='left')

    def on_dropdown(self, _):
        """Refresh the choices in the list using the get_choices function"""
        self.widget['menu'].delete(0, 'end')
        for choice in self.get_choices():
            self.widget['menu'].add_command(label=choice, command=lambda c=choice: self.choose(c))

    def choose(self, choice):
        self.var.set(choice)

    def get_choices(self):
        """Overridden by subclasses, returns all choices valid"""
        return []
