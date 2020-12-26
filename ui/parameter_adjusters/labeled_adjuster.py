"""LabeledAdjuster is a wrapper for other parameter adjusters that puts a label to the left of the adjuster"""
import tkinter as tk


class LabeledAdjuster(tk.Frame):
    def __init__(self, parameter_panel, text, adjuster_type, adjuster_args):
        super().__init__(parameter_panel)
        self.label = tk.Label(self, text=text + ':')
        self.adjuster_type = adjuster_type
        self.adjuster_args = adjuster_args
        self.adjuster = None

    def pack(self, **kwargs):
        self.label.pack(side='left')
        self.adjuster = self.adjuster_type(self, *self.adjuster_args)
        self.adjuster.pack(side='left')
        super().pack(**kwargs)
