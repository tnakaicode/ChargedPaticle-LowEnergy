__all__ = ['TimeGrid', 'TimeGridSection']

from collections import namedtuple

from ef.config.section import ConfigSection
from ef.config.component import ConfigComponent

import TimeGrid as TG


class TimeGrid(ConfigComponent):
    def __init__(self, total=100.0, save_step=10.0, step=1.0):
        self.total = total
        self.save_step = save_step
        self.step = step

    def to_conf(self):
        return TimeGridSection(self.total, self.save_step, self.step)

    def make(self):
        return TG.TimeGrid(self.total, self.step, self.save_step)

    def visualize(self, visualizer):
        pass


class TimeGridSection(ConfigSection):
    section = "TimeGrid"
    ContentTuple = namedtuple("TimeGridTuple", ('total_time', 'time_save_step', 'time_step_size'))
    convert = ContentTuple(float, float, float)

    def make(self):
        return TimeGrid(*self.content)
