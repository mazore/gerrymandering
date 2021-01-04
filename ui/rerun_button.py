import tkinter as tk


class RerunButton(tk.Button):
    def __init__(self, root):
        self.root = root
        super().__init__(command=self.rerun, text='Rerun')

    def rerun(self):
        self.root.focus()  # remove focus from all widgets
        self.root.parameter_panel.on_rerun()
        parameters = self.root.parameter_panel.get_parameters()
        if parameters is None:
            print('at least one parameter is invalid')
            return  # if a parameter is invalid
        self.root.parameters = parameters
        self.root.rerun_simulation()
