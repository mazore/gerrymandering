"""Contains AdjusterType subclasses that are directly used by ParameterPanel"""
from .adjuster_types import CheckboxAdjusterType, EntryAdjusterType, PickerAdjusterType
import inspect
from math import sqrt
from misc import call_or_none
from simulation import BLUE, RED
import sys


class FavorTieAdjuster(CheckboxAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'favor_tie', False, update_on_change=True)


class NumSwapsAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'num_swaps', 'none')
        self.result_formatter = call_or_none(int)


class SimulationTimeAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'simulation_time', 'none')
        self.result_formatter = call_or_none(float)


class DistrictSizeAdjuster(PickerAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'district_size', 16)

        self.get_choices = lambda: [i * i for i in range(2, 10)]
        self.result_formatter = call_or_none(int)

    def after_choice(self, choice):
        self.parameter_panel.adjusters['grid_width'].test_invalid()


class GridWidthAdjuster(PickerAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'grid_width', 24)

        self.result_formatter = call_or_none(int)

    def get_choices(self):
        """Get choices for grid_width based on current set district_size"""
        district_width = int(sqrt(self.parameter_panel.get_parameter('district_size')))
        return [districts_per_row * district_width for districts_per_row in range(2, 15)]

    def test_invalid(self):
        if self.get() not in self.get_choices():
            self.set('invalid')


class HelpPartyAdjuster(PickerAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'help_party', 'blue', update_on_change=True)

        self.get_choices = lambda: ['blue', 'red']
        self.result_formatter = lambda value: {'blue': BLUE, 'red': RED}[value]  # Get Party object from party name

    def after_choice(self, choice):
        """Set the hinder_party parameter to the opposite of help_party"""
        hinder_party = {'red': BLUE, 'blue': RED}[choice.name]
        if self.parameter_panel.root.parameters.hinder_party != hinder_party:  # if different
            self.parameter_panel.set_parameter('hinder_party', hinder_party)
            for district in self.parameter_panel.root.canvas.districts:
                district.net_advantage *= -1


def is_adjuster(obj):
    return inspect.isclass(obj) and obj.__name__.endswith('Adjuster')


all_adjusters = [item[1] for item in inspect.getmembers(sys.modules[__name__], is_adjuster)]
