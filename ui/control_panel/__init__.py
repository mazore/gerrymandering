from .buttons import *
import tkinter as tk


class ControlPanel(tk.Frame):
    """A box that contains control buttons that rerun, pause/resume, show/hide districts, and does one swap"""

    def __init__(self, root):
        self.root = root
        super().__init__(root.ui_frame, bd=1, relief='solid')

        self.rerun_button = RerunButton(self)
        self.pause_resume_button = PauseResumeButton(self)
        self.toggle_districts_button = ToggleDistrictsButton(self)
        self.swap_button = SwapButton(self)

        self.rerun_button.pack(side='left')
        self.pause_resume_button.pack(side='left')
        self.toggle_districts_button.pack(side='left')
        self.swap_button.pack(side='left')
