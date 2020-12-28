from .parameter_adjuster import ParameterAdjuster
import tkinter as tk


class ChoicePicker(ParameterAdjuster):
    """An adjuster type that can be used to choose an item from a list of (or function that returns) choices"""

    def __init__(self, parameter_panel, name, default):
        super().__init__(parameter_panel, name, tk.StringVar(value=default))

        self.widget = tk.OptionMenu(self.frame, self.var, [])
        self.widget.bind('<Button-1>', self.on_dropdown)
        self.widget.pack(side='left')

    def on_dropdown(self, _):
        """Refresh the choices in the list using the get_choices function"""
        self.widget['menu'].delete(0, 'end')
        for choice in self.get_choices():
            self.widget['menu'].add_command(label=choice, command=lambda c=choice: self.on_choice(c))

    def on_choice(self, choice):
        self.var.set(choice)
        self.after_choice()

    def get_choices(self):
        return []

    def after_choice(self):
        pass
