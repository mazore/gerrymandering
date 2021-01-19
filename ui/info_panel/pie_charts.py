from math import cos, sin, radians
from simulation import BLUE, RED
import tkinter as tk


class PieChart:
    def __init__(self, pie_charts, coords, name, get_score, quantity):
        self.pie_charts = pie_charts
        self.get_score, self.quantity = get_score, quantity
        score = get_score()
        pie_charts.create_text((coords[0] + coords[2]) / 2, 0, text=name, font=pie_charts.root.font, anchor='n')
        pie_charts.create_oval(*coords, fill='gray')
        self.blue_id = pie_charts.create_arc(*coords, fill=BLUE.color, start=90, extent=score['blue'] / quantity * 360)
        self.red_id = pie_charts.create_arc(*coords, fill=RED.color, start=90, extent=-score['red'] / quantity * 360)
        self.blue_text_id = pie_charts.create_text(*self.arc_mid(self.blue_id), text=score['blue'], fill='white')
        self.red_text_id = pie_charts.create_text(*self.arc_mid(self.red_id), text=score['red'], fill='white')

    def arc_mid(self, arc_id):
        start = float(self.pie_charts.itemcget(arc_id, 'start'))
        extent = float(self.pie_charts.itemcget(arc_id, 'extent'))
        end = start + extent
        mid_angle = radians((start + end) / 2)
        x1, y1, x2, y2 = self.pie_charts.coords(arc_id)
        r = (x2 - x1) / 4
        center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
        return center_x + cos(mid_angle) * r, center_y - sin(mid_angle) * r

    def update_info(self):
        score = self.get_score()
        self.pie_charts.itemconfig(self.blue_id, extent=score['blue'] / self.quantity * 360)
        self.pie_charts.itemconfig(self.red_id, extent=-score['red'] / self.quantity * 360)
        self.pie_charts.itemconfig(self.blue_text_id, text=score['blue'])
        self.pie_charts.itemconfig(self.red_text_id, text=score['red'])


class PieCharts(tk.Canvas):
    def __init__(self, info_panel):
        self.root = info_panel.root
        super().__init__(info_panel, width=200, height=100)

        def get_score_people():
            score = dict(blue=0, red=0)
            for person in self.root.canvas.iter_people():
                score[person.party.name] += 1
            return score

        get_score_districts = self.root.canvas.get_score
        num_people = self.root.parameters.grid_width ** 2
        num_districts = self.root.canvas.parameters.num_districts

        self.people_chart = PieChart(self, (10, 20, 90, 100), 'population', get_score_people, num_people)
        self.district_chart = PieChart(self, (110, 20, 190, 100), 'districts', get_score_districts, num_districts)

    def update_info(self):
        self.people_chart.update_info()
        self.district_chart.update_info()
