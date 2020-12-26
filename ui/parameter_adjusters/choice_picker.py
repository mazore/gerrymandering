"""ChoicePicker is a parameter adjuster that can be used to select an item from a list of choices"""
import tkinter as tk


class ChoicePicker(tk.OptionMenu):
    def __init__(self, parent, choices):
        self.var = tk.StringVar()
        super().__init__(parent, self.var, *choices)
