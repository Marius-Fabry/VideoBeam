"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

import yfinance
import math
from datetime import datetime, timedelta
from DataSources.Signal import Signal


class YFinSignalFactory:
    def __init__(self, ticker_symbol):
        self.ticker = yfinance.Ticker(ticker_symbol)
        self.ticker_symbol = ticker_symbol

    def get_signal(self, start_time, end_time, interval):
        signal = Signal(self.ticker_symbol)

        one_day = timedelta(days=1)
        five_days = timedelta(days=5)
        one_week = timedelta(days=7)
        one_month = timedelta(days=30)
        one_quarter = timedelta(days=90)

        if interval <= one_day:
            interval_str = "1d"
        elif interval <= five_days:
            interval_str = "5d"
        elif interval <= one_week:
            interval_str = "1wk"
        elif interval <= one_month:
            interval_str = "1mo"
        elif interval <= one_quarter:
            interval_str = "3mo"
        else:
            interval_str = "1mo"

        df = self.ticker.history(
            interval=interval_str, start=start_time, end=end_time)

        for date, values in df.iterrows():
            closing_price = values['Close']
            if math.isnan(closing_price):
                continue
            signal.add_data_point(Signal.DataPoint(
                datetime.fromisoformat(str(date)), closing_price))

        return signal
