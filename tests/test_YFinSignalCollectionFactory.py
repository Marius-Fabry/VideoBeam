"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

import unittest
from datetime import datetime, timedelta
from DataSources.YFinSignalCollectionFactory import YFinSignalCollectionFactory


class TestYFinSignalCollectionFactory(unittest.TestCase):
    def setUp(self):
        self.factory = YFinSignalCollectionFactory(["MSFT", "AAPL"])

    def test_construction(self):
        YFinSignalCollectionFactory(["bla", "blubb"])

    def test_get_signals(self):
        start_time = datetime.fromisoformat("2019-01-01")
        end_time = datetime.fromisoformat("2020-01-01")
        interval = timedelta(days=30)
        collection = self.factory.get_signal_collection(
            start_time, end_time, interval)
        self.assertGreater(len(collection.get_signals()), 0)
