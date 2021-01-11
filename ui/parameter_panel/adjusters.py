"""Contains AdjusterType subclasses that are directly used by ParameterPanel"""
from .adjuster_types import *
import inspect
from math import sqrt
from simulation import BLUE, RED
import sys


class FavorTieAdjuster(CheckboxAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'favor_tie', update_on_change=True)


class CanvasWidthAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'canvas_width', 480, int)


class LineWidthAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'line_width', 3, int, width=4)


class NumSwapsAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'num_swaps', 1000, int, use_checkbutton=True)


class NumSwapsPerDrawAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'num_swaps_per_draw', 1, int)


class SimulationTimeAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'simulation_time', 2, float, use_checkbutton=True, width=4)


class SleepBetweenDrawsAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'sleep_between_draws', 0, int)


class DistrictSizeAdjuster(PickerAdjusterType):
    def __init__(self, parameter_panel):
        self.get_obj_from_str = int
        super().__init__(parameter_panel, 'district_size')

        self.get_choices = lambda: [i * i for i in range(2, 10)]

    def after_choice(self, choice):
        self.parameter_panel.adjusters['grid_width'].test_invalid()


class GridWidthAdjuster(PickerAdjusterType):
    def __init__(self, parameter_panel):
        self.get_obj_from_str = int
        super().__init__(parameter_panel, 'grid_width')

    def get_choices(self):
        """Get choices for grid_width based on current set district_size"""
        district_width = int(sqrt(self.parameter_panel.get_parameter('district_size')))
        return [districts_per_row * district_width for districts_per_row in range(2, 15)]

    def test_invalid(self):
        if self.get() not in self.get_choices():
            self.set('invalid')


class HelpPartyAdjuster(PickerAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'help_party', update_on_change=True)

        self.get_choices = lambda: [BLUE, RED]

    def after_choice(self, choice):
        """Set the hinder_party parameter to the opposite of help_party"""
        hinder_party = {'red': BLUE, 'blue': RED}[choice.name]
        if self.parameter_panel.root.parameters.hinder_party != hinder_party:  # if different
            self.parameter_panel.set_parameter('hinder_party', hinder_party)
            for district in self.parameter_panel.root.canvas.districts:
                district.net_advantage *= -1

    def get_obj_from_str(self, s):
        return {'blue': BLUE, 'red': RED}[s]


def is_adjuster(obj):
    return inspect.isclass(obj) and obj.__name__.endswith('Adjuster')


all_adjusters = [item[1] for item in inspect.getmembers(sys.modules[__name__], is_adjuster)]
