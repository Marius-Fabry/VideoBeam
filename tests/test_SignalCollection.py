"""    
This file is part of VideoBeam.

VideoBeam is software written by Marius Fabry.
"""

import unittest
from datetime import datetime, timedelta
from DataSources.SignalCollection import SignalCollection
from DataSources.RandomSignalFactory import RandomSignalFactory


class TestSignalCollection(unittest.TestCase):
    def setUp(self):
        self.start_date = datetime.fromisoformat("2019-01-01")
        self.end_date = self.start_date + timedelta(days=10)
        self.signal_collection = self._construct_test_collection()

    def test_constuction(self):
        SignalCollection([])

    def test_get_signals(self):
        self.signal_collection.get_signals()

    def test_get_max_value(self):
        value = self.signal_collection.get_max_value()
        self.assertGreater(value, 0)

    def test_get_max_value(self):
        value = self.signal_collection.get_max_value_up_to_date(
            self.start_date + timedelta(days=2))
        self.assertGreater(value, 0)

    def test_get_indices_sorted_by_value_at_date(self):
        test_date = self.start_date + timedelta(days=1)
        sorted_indices = self.signal_collection.get_indices_sorted_by_value_at_date(
            test_date)
        signals = []
        for idx in sorted_indices:
            signal = self.signal_collection.get_signals()[idx]
            signals.append(signal)
        assert(signals[0].get_value(test_date) >=
               signals[1].get_value(test_date))
        assert(signals[1].get_value(test_date) >=
               signals[2].get_value(test_date))

    def test_get_earliest_date(self):
        begin = self.signal_collection.get_earliest_date()
        self.assertEqual(begin, self.start_date)

    def test_get_latest_date(self):
        end = self.signal_collection.get_latest_date()
        self.assertEqual(end, self.end_date)

    def _construct_test_collection(self):
        signals = []
        signal_factory = RandomSignalFactory()
        interval = timedelta(days=1)
        for _ in range(3):
            signals.append(signal_factory.get_signal(
                self.start_date, self.end_date, interval))
        return SignalCollection(signals)
