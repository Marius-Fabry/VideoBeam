"""    
This file is part of VideoBeam.

VideoBeam is software written by Marius Fabry.
"""

import os
import unittest
from datetime import datetime, timedelta
from Rendering.Renderer import Renderer, RendererConfig
from DataSources.RandomSignalFactory import RandomSignalFactory
from DataSources.SignalCollection import SignalCollection


class TestRenderer(unittest.TestCase):

    def test_rendering(self):
        # given
        testvideo_basefilename = "./testvideo"
        testvideo_fullfilename = testvideo_basefilename + ".mp4"
        renderer = self._test_rendering_given(testvideo_basefilename)
        # when
        renderer.render_frames()
        # then
        self.assertTrue(os.path.exists(testvideo_fullfilename))

    def _test_rendering_given(self, testvideo_basefilename):
        render_cfg = RendererConfig()
        render_cfg.basefilename = testvideo_basefilename
        render_cfg.start_date = datetime.fromisoformat("2019-01-01")
        render_cfg.end_date = render_cfg.start_date + timedelta(days=15)
        render_cfg.frame_time_interval = timedelta(days=1)
        render_cfg.start_frames = 30
        render_cfg.end_frames = 5
        render_cfg.video_title = "My Test Video"
        testvideo_fullfilename = testvideo_basefilename + ".mp4"
        signals = self._construct_test_signals()
        try:
            os.remove(testvideo_fullfilename)
        except:
            pass
        return Renderer(SignalCollection(signals), render_cfg)

    def _construct_test_signals(self):
        signals = []
        signal_factory = RandomSignalFactory()
        start_time = datetime.fromisoformat("2019-01-01")
        end_time = start_time + timedelta(days=15)
        interval = timedelta(days=1)
        for _ in range(3):
            signals.append(signal_factory.get_signal(
                start_time, end_time, interval))
        return signals
