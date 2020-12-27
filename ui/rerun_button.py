import tkinter as tk


class RerunButton(tk.Button):
    def __init__(self, root):
        self.root = root
        super().__init__(command=self.command, text='Rerun')

    def command(self):
        self.root.parameters = self.root.parameter_adjusters.get_parameters()
        self.root.rerun_simulation()
