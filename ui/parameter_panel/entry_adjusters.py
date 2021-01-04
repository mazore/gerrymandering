"""Contains Entry subclasses that are directly used by ParameterPanel"""
from .entry_adjuster_type import EntryAdjusterType
from misc import call_or_none


class NumSwapsAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'num_swaps', 'none')
        self.result_formatter = call_or_none(int)


class SimulationTimeAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'simulation_time', 'none')
        self.result_formatter = call_or_none(float)
