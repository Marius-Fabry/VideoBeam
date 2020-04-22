"""    
This file is part of VideoBeam.

VideoBeam is software written by Marius Fabry.
"""

import unittest
from datetime import datetime, timedelta
from DataSources.YFinSignalFactory import YFinSignalFactory


class TestYFinSignalFactory(unittest.TestCase):
    def setUp(self):
        self.factory = YFinSignalFactory("MSFT")
        self.start_date = datetime.fromisoformat("2019-01-01")
        self.end_date = self.start_date + timedelta(days=100)

    def test_construction(self):
        YFinSignalFactory("SOMESYMBOL")

    def test_get_signal_collection(self):
        signal = self.factory.get_signal(
            self.start_date, self.end_date, timedelta(days=1))
        self.assertGreater(len(signal.get_data_points()), 0)
