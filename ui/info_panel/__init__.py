from .pie_charts import PieCharts
from .swaps_done_info import SwapsDoneInfo
import tkinter as tk


class InfoPanel(tk.Frame):
    """A box that contains information like how many swaps done, how many districts per party, etc."""

    def __init__(self, root):
        self.root = root
        super().__init__(root.ui_frame, bd=1, relief='solid')

        self.pie_charts = PieCharts(self)
        self.swaps_done_info = SwapsDoneInfo(self)

        self.pie_charts.pack(side='top')
        self.swaps_done_info.pack(side='top')

        self.after_id = self.root.after(10, self.update_info)

    def on_restart(self):
        self.pie_charts.on_restart()

    def update_info(self):
        self.pie_charts.update_info()
        self.swaps_done_info.update_info()
        self.after_id = self.root.after(100, self.update_info)
