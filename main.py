"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

from DataSources.YFinSignalCollectionFactory import YFinSignalCollectionFactory
from DataSources.SignalCollection import SignalCollection
from Rendering.Renderer import Renderer, RendererConfig
from datetime import datetime, timedelta


def main():
    collectionfactory = YFinSignalCollectionFactory(
        ["FB", "AAPL", "AMZN", "NFLX", "GOOGL"])
    start = datetime.fromisoformat("2000-01-01")
    end = datetime.fromisoformat("2020-04-17")
    interval = timedelta(days=30)
    signal_collection = collectionfactory.get_signal_collection(
        start, end, interval)
    renderer_cfg = RendererConfig()
    renderer_cfg.start_date = signal_collection.get_earliest_date()
    renderer_cfg.end_date = signal_collection.get_latest_date()
    renderer_cfg.frame_time_interval = timedelta(days=1)
    renderer_cfg.basefilename = "out"
    renderer_cfg.video_title = "FAANG Stock Prices 2000-2020"
    renderer = Renderer(signal_collection, renderer_cfg)
    renderer.render_frames()


if __name__ == "__main__":
    main()
