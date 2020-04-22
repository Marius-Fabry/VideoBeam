"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

from DataSources.Signal import Signal
from datetime import datetime


class SignalCollection:
    def __init__(self, signals):
        if len(signals) > 0:
            for signal in signals:
                assert(type(signal) == Signal)
        self.signals = signals

    def get_signals(self):
        return self.signals

    def get_indices_sorted_by_value_at_date(self, date):
        signal_indices = range(0, len(self.signals))
        signal_indices = sorted(
            signal_indices, key=lambda x: self.signals[x].get_value(date), reverse=True)
        return signal_indices

    def get_max_value(self):
        max_value = 0
        for signal in self.signals:
            for datapoint in signal.get_data_points():
                max_value = max(max_value, datapoint.get_value())
        if max_value == 0:
            max_value = 1
        return max_value

    def get_max_value_up_to_date(self, date):
        max_value = 0
        for signal in self.signals:
            for datapoint in signal.get_data_points():
                if datapoint.get_timestamp() > date:
                    max_value = max(max_value, signal.get_value(date))
                    break
                max_value = max(max_value, datapoint.get_value())
        if max_value == 0:
            max_value = 1
        return max_value

    def get_earliest_date(self):
        if len(self.signals) == 0:
            return None
        date = datetime(year=9999, month=12, day=31)
        for signal in self.signals:
            datapoints = signal.get_data_points()
            if len(datapoints) > 0:
                date = min(date, datapoints[0].get_timestamp())
        return date

    def get_latest_date(self):
        if len(self.signals) == 0:
            return None
        date = datetime(year=1, month=1, day=1)
        for signal in self.signals:
            datapoints = signal.get_data_points()
            if len(datapoints) > 0:
                date = max(date, datapoints[-1].get_timestamp())
        return date
