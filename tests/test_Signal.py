"""    
This file is part of VideoBeam.

VideoBeam is software written by Marius Fabry.
"""

import unittest
from datetime import datetime
from DataSources.Signal import Signal


class TestSignal(unittest.TestCase):
    def test_construction(self):
        self.construct_test_signal()

    def test_get_name(self):
        raw_signal = self.construct_test_signal()
        raw_signal.get_name()

    def test_add_data_points(self):
        raw_signal = self.construct_test_signal()
        some_time = datetime.now()
        some_value = 1337
        some_data_point = Signal.DataPoint(some_time, some_value)
        raw_signal.add_data_point(some_data_point)
        raw_signal.add_data_point(some_data_point)
        raw_signal.add_data_point(some_data_point)

    def test_get_max_value(self):
        raw_signal = self.construct_test_signal()
        some_time = datetime.now()
        some_value = 1337
        some_data_point = Signal.DataPoint(some_time, some_value)
        raw_signal.add_data_point(some_data_point)
        some_time = datetime.now()
        some_value = 42
        some_data_point = Signal.DataPoint(some_time, some_value)
        raw_signal.add_data_point(some_data_point)
        self.assertEqual(raw_signal.get_max_value(), 1337)

    def test_interpolation(self):
        signal = Signal("Some Signal")
        first_time = datetime.fromisoformat("2019-01-01")
        first_value = 0.0
        first_data_point = Signal.DataPoint(first_time, first_value)
        signal.add_data_point(first_data_point)
        second_time = datetime.fromisoformat("2020-01-01")
        second_value = 1.0
        second_data_point = Signal.DataPoint(second_time, second_value)
        signal.add_data_point(first_data_point)
        signal.add_data_point(second_data_point)
        query_time = datetime.fromisoformat("2019-07-01")
        interpolated_data = signal.get_value(query_time)
        self.assertAlmostEqual(interpolated_data, 0.5, places=2)

    def construct_test_signal(self):
        return Signal("Some Signal")


class TestSignalDataPoint(unittest.TestCase):
    def test_construction(self):
        some_time = datetime.now()
        some_value = 1337
        Signal.DataPoint(some_time, some_value)
