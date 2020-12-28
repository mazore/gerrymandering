import tkinter as tk


class ParameterAdjuster:
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
        return value
