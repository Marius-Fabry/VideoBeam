"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

from DataSources.Signal import Signal
import random


class RandomSignalFactory:
    def __init__(self):
        self.signals_produced = 0

    def get_signal(self, start_time, end_time, interval):
        signal = Signal("Signal " + str(self.signals_produced))
        self.signals_produced += 1
        time = start_time
        value = 0
        while time != (end_time + interval):
            signal.add_data_point(Signal.DataPoint(time, value))
            value += random.uniform(10.0, 1000.0)
            time += interval
        return signal
