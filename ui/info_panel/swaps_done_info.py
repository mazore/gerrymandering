import tkinter as tk


class SwapsDoneInfo(tk.Label):
    def __init__(self, info_panel):
        self.root = info_panel.root
        self.var = tk.StringVar()
        self.update_info()
        super().__init__(info_panel, textvariable=self.var)

    def update_info(self):
        self.var.set(f'swaps_done: {self.root.canvas.swap_manager.swaps_done}')
