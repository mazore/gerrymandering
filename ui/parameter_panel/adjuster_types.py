from .parameter_adjuster_base import ParameterAdjusterBase
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
        assert ValueError


class EntryAdjusterType(ParameterAdjusterBase):
    """Can be used to enter a value into a field"""

    def __init__(self, parameter_panel, name, disabled_value, type_, width=5, **kwargs):
        self.type = type_
        super().__init__(parameter_panel, name, pad_y=3, **kwargs)

        self.checkbutton_var = tk.BooleanVar(value=self.var.get() != 'None')
        self.checkbutton_var.trace('w', self.update_disabled)
        self.checkbutton = tk.Checkbutton(self.frame, variable=self.checkbutton_var)
        self.checkbutton.pack(side='left')

        self.widget = tk.Entry(self.frame, font=self.normal_font, textvariable=self.var, width=width, relief='solid')
        self.widget.pack(side='left')
        self.widget.bind('<Return>', lambda _: self.parameter_panel.root.focus())
        if self.var.get() == 'None':
            self.var.set(disabled_value)
        self.update_disabled()

    def get_obj_from_str(self, s):
        if not self.checkbutton_var.get():
            return None
        try:
            return self.type(s)
        except ValueError:
            return None

    def update_disabled(self, *_):
        if self.checkbutton_var.get():
            self.widget.configure(relief='solid', state='normal')
        else:
            self.widget.configure(relief='sunken', state='disabled')


class PickerAdjusterType(ParameterAdjusterBase):
    """Can be used to choose an item from a list of (or function that returns) choices, shown as a dropdown list"""

    def __init__(self, parameter_panel, name, **kwargs):
        super().__init__(parameter_panel, name, **kwargs)

        self.widget = tk.OptionMenu(self.frame, self.var, None)
        self.widget.config(font=self.normal_font)
        self.widget.bind('<Button-1>', self.on_dropdown)
        self.widget.pack(side='left')

    def on_dropdown(self, _):
        """Refresh the choices in the list using the get_choices function"""
        self.widget['menu'].delete(0, 'end')
        for choice in self.get_choices():
            self.widget['menu'].add_command(label=choice, font=self.normal_font,
                                            command=lambda c=choice: self.choose(c))

    def choose(self, choice):
        self.var.set(choice)

    def get_choices(self):
        """Overridden by subclasses, returns all choices valid"""
        return []
