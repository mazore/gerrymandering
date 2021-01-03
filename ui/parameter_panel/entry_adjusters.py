"""Contains Entry subclasses that are directly used by ParameterPanel"""
from .entry_adjuster_type import EntryAdjusterType


class NumSwapsAdjuster(EntryAdjusterType):
    def __init__(self, parameter_panel):
        super().__init__(parameter_panel, 'district_size', 16)
