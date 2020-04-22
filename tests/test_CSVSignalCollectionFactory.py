"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

import unittest
from DataSources.CSVSignalCollectionFactory import CSVSignalCollectionFactory


class TestCSVSignalCollectionFactory(unittest.TestCase):
    def test_construction(self):
        CSVSignalCollectionFactory("")

    def test_csv_import(self):
        factory = CSVSignalCollectionFactory("data/testdata.csv")
        signalcollection = factory.get_signal_collection()
        signals = signalcollection.get_signals()
        self.assertEqual(len(signals), 3)
        self.assertEqual(signals[0].get_name(), "Signal 1")
        self.assertEqual(signals[1].get_name(), "Signal 2")
        self.assertEqual(signals[2].get_name(), "Signal 3")
        self.assertNotEqual(len(signals[0].get_data_points()), 0)
        self.assertNotEqual(len(signals[1].get_data_points()), 0)
        self.assertNotEqual(len(signals[2].get_data_points()), 0)

    def test_S_and_P_500_import(self):
        factory = CSVSignalCollectionFactory("data_not_shared/s&p500.csv")
        signalcollection = factory.get_signal_collection()
        signals = signalcollection.get_signals()
        self.assertEqual(len(signals), 9)
