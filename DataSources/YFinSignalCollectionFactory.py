"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

from DataSources.YFinSignalFactory import YFinSignalFactory
from DataSources.SignalCollection import SignalCollection


class YFinSignalCollectionFactory:
    def __init__(self, ticker_symbols):
        self.ticker_symbols = ticker_symbols

    def get_signal_collection(self, start_time, end_time, interval):
        signals = []
        for symbol in self.ticker_symbols:
            factory = YFinSignalFactory(symbol)
            signals.append(factory.get_signal(start_time, end_time, interval))
        return SignalCollection(signals)
