"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

import random
import csv
from datetime import datetime
from DataSources.Signal import Signal
from DataSources.SignalCollection import SignalCollection


class CSVSignalCollectionFactory:
    def __init__(self, filename):
        self.filename = filename

    def get_signal_collection(self):
        signals = self._read_file()
        return SignalCollection(signals)

    def _read_file(self):
        signals = []
        with open(self.filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                cell_count = 0
                if line_count == 0:
                    for cell in row:
                        if cell_count == 0:
                            pass
                        else:
                            signals.append(Signal(cell))
                        cell_count += 1
                else:
                    date = None
                    for cell in row:
                        if cell_count == 0:
                            date = datetime.fromisoformat(cell)
                        elif cell != "":
                            signals[cell_count -
                                    1].add_data_point(Signal.DataPoint(date, float(cell)))
                        cell_count += 1
                    line_count += 1
                line_count += 1
        return signals
