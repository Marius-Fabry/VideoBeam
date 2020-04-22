"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

from datetime import datetime, timedelta


class Signal:
    def __init__(self, name, unit='$'):
        self.name = name
        self.data_points = []
        self.unit = unit

    def get_name(self):
        return self.name

    def add_data_point(self, data_point):
        assert(type(data_point) == Signal.DataPoint)
        self.data_points.append(data_point)

    def get_data_points(self):
        return self.data_points

    def get_unit(self):
        return self.unit

    def get_max_value(self):
        return max(d.get_value() for d in self.data_points)

    def get_value(self, timestamp):
        if len(self.data_points) == 0:
            return None
        first_datapoint = self.data_points[0]
        second_datapoint = self.data_points[0]
        last_datapoint = self.data_points[0]

        if timestamp < first_datapoint.get_timestamp():
            return 0

        for datapoint in self.data_points:
            if datapoint.get_timestamp() > timestamp:
                first_datapoint = last_datapoint
                second_datapoint = datapoint
                break
            last_datapoint = datapoint
            second_datapoint = datapoint
        if timestamp > second_datapoint.get_timestamp():
            return second_datapoint.get_value()
        value = self._interpolate_between_datapoints(
            first_datapoint, second_datapoint, timestamp)
        return value

    def _interpolate_between_datapoints(self, first_datapoint, second_datapoint, timestamp):
        value_base = first_datapoint.get_value()
        value_diff = second_datapoint.get_value() - first_datapoint.get_value()
        time_diff = second_datapoint.get_timestamp() - first_datapoint.get_timestamp()
        interp_time_diff = timestamp - first_datapoint.get_timestamp()
        if self._is_timedelta_zero(time_diff):
            interp_factor = 0.0
        else:
            interp_factor = interp_time_diff / time_diff
        return value_base + interp_factor * value_diff

    def _is_timedelta_zero(self, delta):
        return delta == timedelta()

    class DataPoint():
        def __init__(self, timestamp, value):
            assert(type(timestamp) == datetime)
            self.timestamp = timestamp
            self.value = value

        def get_timestamp(self):
            return self.timestamp

        def get_value(self):
            return self.value
