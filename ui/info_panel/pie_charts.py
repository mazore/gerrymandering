from math import cos, sin, radians
from simulation import BLUE, RED
import tkinter as tk


class PieChart:
    def __init__(self, pie_charts, coords, name, get_score, get_quantity):
        self.pie_charts = pie_charts
        self.get_score, self.get_quantity = get_score, get_quantity
        self.score, self.quantity = self.get_score(), self.get_quantity()
        pie_charts.create_text((coords[0] + coords[2]) / 2, 0, text=name, font=pie_charts.root.font, anchor='n')
        pie_charts.create_oval(*coords, fill='gray', outline='white')  # Tied part
        self.blue_id = pie_charts.create_arc(*coords, fill=BLUE.color, start=90,
                                             extent=self.score['blue'] / self.quantity * 360, outline='white')
        self.red_id = pie_charts.create_arc(*coords, fill=RED.color, start=90,
                                            extent=-self.score['red'] / self.quantity * 360, outline='white')
        self.blue_text_id = pie_charts.create_text(*self.arc_mid(self.blue_id), text=self.score['blue'], fill='white')
        self.red_text_id = pie_charts.create_text(*self.arc_mid(self.red_id), text=self.score['red'], fill='white')

    def arc_mid(self, arc_id):
        """Returns the midpoint of the line between the center and the midpoint of the arc"""
        start, extent = self.pie_charts.itemcget(arc_id, 'start'), self.pie_charts.itemcget(arc_id, 'extent')
        mid_angle = radians(float(start) + float(extent) / 2)
        x1, y1, x2, y2 = self.pie_charts.coords(arc_id)
        center_x, center_y, r = (x1 + x2) / 2, (y1 + y2) / 2, (x2 - x1) / 2
        return center_x + cos(mid_angle) * r / 2, center_y - sin(mid_angle) * r / 2

    def on_restart(self):
        self.quantity = self.get_quantity()  # Recalculate quantity

    def update_info(self):
        current_score = self.get_score()
        if self.score == current_score:
            return  # If no change
        self.score = current_score
        self.pie_charts.itemconfig(self.blue_id, extent=self.score['blue'] / self.quantity * 360)
        self.pie_charts.itemconfig(self.red_id, extent=-self.score['red'] / self.quantity * 360)
        self.pie_charts.itemconfig(self.blue_text_id, text=self.score['blue'])
        self.pie_charts.itemconfig(self.red_text_id, text=self.score['red'])
        self.pie_charts.coords(self.blue_text_id, *self.arc_mid(self.blue_id))
        self.pie_charts.coords(self.red_text_id, *self.arc_mid(self.red_id))


class PieCharts(tk.Canvas):
    def __init__(self, info_panel):
        self.root = info_panel.root
        super().__init__(info_panel, width=200, height=100)

        self.people_chart = PieChart(self, (10, 20, 90, 100), 'population',
                                     self.get_score_people, self.get_quantity_people)
        self.district_chart = PieChart(self, (110, 20, 190, 100), 'districts',
                                       self.get_score_districts, self.get_quantity_districts)

    def on_restart(self):
        self.people_chart.on_restart()
        self.people_chart.update_info()
        self.district_chart.on_restart()

    def update_info(self):
        self.district_chart.update_info()

    def get_score_people(self):
        score = dict(blue=0, red=0)
        for person in self.root.canvas.iter_people():
            score[person.party.name] += 1
        return score

    def get_score_districts(self):
        return self.root.canvas.get_score()

    def get_quantity_people(self):
        return self.root.parameters.grid_width ** 2

    def get_quantity_districts(self):
        return self.root.canvas.parameters.num_districts
