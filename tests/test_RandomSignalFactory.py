"""    
This file is part of VideoBeam.

VideoBeam is software written by Marius Fabry.
"""

import unittest
import pprint
from datetime import datetime, timedelta
from DataSources.RandomSignalFactory import RandomSignalFactory


class TestRandomSignalFactory(unittest.TestCase):
    def test_construction(self):
        RandomSignalFactory()

    def test_get_signal(self):
        factory = RandomSignalFactory()
        start_time = datetime.fromisoformat("2019-01-01")
        end_time = start_time + timedelta(days=99)
        interval = timedelta(days=1)
        signal = factory.get_signal(start_time, end_time, interval)
        datapoints = signal.get_data_points()
        self.assertEqual(len(datapoints), 100)
