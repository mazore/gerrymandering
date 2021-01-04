from .parameter_adjuster_base import ParameterAdjusterBase
import tkinter as tk


class EntryAdjusterType(ParameterAdjusterBase):
    def __init__(self, parameter_panel, name, default):
        super().__init__(parameter_panel, name, tk.StringVar(value=default), pad_y=3)

        self.widget = tk.Entry(self.frame, textvariable=self.var, width=5, relief='solid')
        self.widget.config(font=self.normal_font)
        self.widget.pack(side='left')
