from .choice_picker import ChoicePicker
from math import sqrt
from simulation import BLUE, RED


def to_int_or_none(value):
    return int(value) if value else None


class DistrictSizeAdjuster(ChoicePicker):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'district_size', 16)

        self.get_choices = lambda: [i*i for i in range(2, 10)]
        self.result_formatter = to_int_or_none

    def after_choice(self):
        grid_width = self.parameter_panel.get_parameter('grid_width')
        grid_width_adjuster = self.parameter_panel.adjusters['grid_width']
        if grid_width not in grid_width_adjuster.get_choices():
            grid_width_adjuster.set('invalid')


class GridWidthAdjuster(ChoicePicker):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'grid_width', 24)

        self.result_formatter = to_int_or_none

    def get_choices(self):
        district_width = int(sqrt(self.parameter_panel.get_parameter('district_size')))
        return [districts_per_row * district_width for districts_per_row in range(2, 15)]


class HelpPartyAdjuster(ChoicePicker):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'help_party', 'blue')

        self.get_choices = lambda: ['blue', 'red']

    def after_choice(self):
        help_party = self.parameter_panel.get_parameter('help_party')
        hinder_party = {'red': BLUE, 'blue': RED}[help_party.name]

        root = self.parameter_panel.root
        canvas = root.canvas
        if root.parameters.help_party != help_party:  # if a change happened
            root.parameters.help_party = canvas.parameters.help_party = help_party
            root.parameters.hinder_party = canvas.parameters.hinder_party = hinder_party
            for district in canvas.districts:
                district.net_advantage *= -1

    def result_formatter(self, value):
        return {'blue': BLUE, 'red': RED}[value]
