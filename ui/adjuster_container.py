import tkinter as tk


class AdjusterContainer:
    """Contains an adjuster and a label for that adjuster"""
    def __init__(self, parent, adjuster_type, name, *args, **kwargs):
        self.name = name
        frame = tk.Frame(parent)
        tk.Label(frame, text=name + ':').pack(side='left')
        self.adjuster = adjuster_type(frame, *args, **kwargs)
        self.adjuster.pack(side='left')
        frame.pack(side='top')
