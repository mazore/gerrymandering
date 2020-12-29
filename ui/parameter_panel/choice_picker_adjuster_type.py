from .parameter_adjuster_base import ParameterAdjusterBase
import tkinter as tk


class ChoicePickerAdjusterType(ParameterAdjusterBase):
    """An adjuster type that can be used to choose an item from a list of (or function that returns) choices, shown as a
    dropdown list"""

    def __init__(self, parameter_panel, name, default):
        super().__init__(parameter_panel, name, tk.StringVar(value=default))

        self.widget = tk.OptionMenu(self.frame, self.var, [])
        self.widget.config(font=self.normal_font)
        self.widget.bind('<Button-1>', self.on_dropdown)
        self.widget.pack(side='left')

    def on_dropdown(self, _):
        """Refresh the choices in the list using the get_choices function"""
        self.widget['menu'].delete(0, 'end')
        for choice in self.get_choices():
            self.widget['menu'].add_command(label=choice, command=lambda c=choice: self.on_choice(c))

    def on_choice(self, choice):
        """Called when an item is selected from the dropdown list"""
        self.var.set(choice)
        self.after_choice()
        self.update_boldness()

    def get_choices(self):
        """Overridden by subclasses, returns all choices valid"""
        return []

    def after_choice(self):
        """Overridden by subclasses, called after an item is selected from the dropdown list. Typically used to ensure
        other entered parameters are valid or actually change a simulation parameter"""
        pass
