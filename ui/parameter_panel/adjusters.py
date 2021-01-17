"""Contains AdjusterType subclasses that are directly used by ParameterPanel"""
from .adjuster_types import *
from math import sqrt
from simulation import BLUE, RED, DrawMode


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


class FavorTieAdjuster(CheckboxAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'favor_tie', update_on_change=True)


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
        district_width = int(sqrt(self.parameter_panel.adjusters['district_size'].get()))
        return [districts_per_row * district_width for districts_per_row in range(2, 15)]

    def test_invalid(self):
        choices = self.get_choices()
        current = self.get()
        if current not in choices:
            closest = min(choices, key=lambda val: abs(val - current))
            self.set(closest)


class CanvasWidthAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'canvas_width', int, min_=50, advanced=True)


class LineWidthAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'line_width', int, min_=0, width=4, advanced=True)


class DrawModeAdjuster(PickerAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'draw_mode', update_on_change=True, advanced=True)

        self.get_choices = lambda: ['normal', 'margins']

    def get_obj_from_str(self, s):
        d = {}
        for enum_obj in DrawMode.__members__.values():
            d[enum_obj.value] = enum_obj
        return d[s]

    def after_choice(self, _):
        [district.draw() for district in self.parameter_panel.root.canvas.districts]


class SleepBetweenDrawsAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'sleep_between_draws', int, min_=0, advanced=True)


class NumSwapsPerDrawAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'num_swaps_per_draw', int, min_=1, advanced=True)


class NumSwapsAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'num_swaps', int,
                         use_checkbutton=True, disabled_value=1000, min_=1, advanced=True)


class SimulationTimeAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'simulation_time', float,
                         use_checkbutton=True, disabled_value=2, width=4, min_=0.1, advanced=True)


all_adjusters = [
    HelpPartyAdjuster,
    FavorTieAdjuster,
    DistrictSizeAdjuster,
    GridWidthAdjuster,
    CanvasWidthAdjuster,
    LineWidthAdjuster,
    DrawModeAdjuster,
    SleepBetweenDrawsAdjuster,
    NumSwapsPerDrawAdjuster,
    NumSwapsAdjuster,
    SimulationTimeAdjuster,
]
