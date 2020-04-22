"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import copy
from datetime import datetime, timedelta
from DataSources.SignalCollection import SignalCollection
from Rendering.SignalVisual import SignalVisual
from Rendering.DrawText import draw_text


class RendererConfig:
    def __init__(self):
        self.video_title = ""
        self.basefilename = "out"
        self.image_size_x = 1920
        self.image_size_y = 1080
        self.lossless = False
        self.lossless_fourcc = 'HFYU'
        self.lossless_extention = '.avi'
        self.compressed_fourcc = 'mp4v'
        self.compressed_extention = '.mp4'
        #self.font_filename = "media/fonts/Cormorant_Install_v3.0/1. TrueType Font Files/Cormorant-Light.ttf"
        #self.title_font_filename = "media/fonts/Cormorant_Install_v3.0/1. TrueType Font Files/Cormorant-Bold.ttf"
        self.font_filename = "media/fonts/Titre/XB Titre Shadow.ttf"
        self.title_font_filename = "media/fonts/Titre/XB Titre Shadow.ttf"
        self.font_size = 32
        self.title_font_size = 64
        self.fps = 60
        self.background_color = (50, 200, 255)
        self.rectangle_fill_color = (0, 0, 0, 120)
        self.text_fill_color = (0, 0, 0)
        self.margin = 30
        self.bar_height = 140
        self.right_image_margin = 200
        self.left_image_margin = 200
        self.date_format = "%b %Y"
        self.start_date = datetime.fromisoformat("2019-01-01")
        self.frame_time_interval = timedelta(hours=1)
        self.end_date = self.start_date + \
            timedelta(seconds=600 * self.frame_time_interval.total_seconds())
        self.start_frames = 60
        self.end_frames = 30
        #self.background_filename = None
        self.background_filename = 'media/bg1.png'


class Renderer:
    def __init__(self, signal_collection, renderer_config=RendererConfig()):
        assert(type(renderer_config) == RendererConfig)
        assert(type(signal_collection) == SignalCollection)
        self.config = renderer_config
        self.signal_collection = signal_collection
        self.signals = signal_collection.get_signals()
        self.signal_visuals = []
        for signal in self.signals:
            self.signal_visuals.append(SignalVisual(signal, self.config))
        self.max_value = 1
        for visual in self.signal_visuals:
            visual.set_max_signal_value(self.max_value)
        self.current_date = self.config.start_date
        self.video_writer = None
        self.font = None
        self.title_font = None
        self.bg_image = None
        self.logo_img = Image.open('media/logo_250_opacity50.png', 'r')

    def render_frames(self):
        self.start_frame_counter = 0
        self.end_frame_counter = 0
        self._setup_video_writer()
        while self._render_next_frame():
            print("Rendered frame: " + str(self.current_date))
            pass

    def _setup_video_writer(self):
        videodims = (self.config.image_size_x, self.config.image_size_y)
        fps = self.config.fps
        if self.config.lossless:
            fourcc = cv2.VideoWriter_fourcc(*self.config.lossless_fourcc)
            self.video_writer = cv2.VideoWriter(
                self.config.basefilename + self.config.lossless_extention, fourcc, fps, videodims)
        else:
            fourcc = cv2.VideoWriter_fourcc(*self.config.compressed_fourcc)
            self.video_writer = cv2.VideoWriter(
                self.config.basefilename + self.config.compressed_extention, fourcc, fps, videodims)
        self.font = ImageFont.truetype(
            self.config.font_filename, self.config.font_size)
        self.title_font = ImageFont.truetype(
            self.config.title_font_filename, self.config.title_font_size)

    def _render_next_frame(self):
        if self.config.background_filename is not None:
            if self.bg_image is None:
                self.bg_image = Image.open(
                    self.config.background_filename, 'r')
            image = copy.copy(self.bg_image)
        else:
            image = Image.new('RGBA', (self.config.image_size_x,
                                       self.config.image_size_y), self.config.background_color)
        overlay = Image.new('RGBA', (self.config.image_size_x,
                                     self.config.image_size_y), (0, 0, 0, 0))

        draw = ImageDraw.Draw(image)
        overlay_draw = ImageDraw.Draw(overlay)

        pos_y = self.config.bar_height

        signal_indices = self.signal_collection.get_indices_sorted_by_value_at_date(
            self.current_date)

        self.max_value = self.signal_collection.get_max_value_up_to_date(
            self.current_date)

        for signal_idx in signal_indices:
            signal_visual = self.signal_visuals[signal_idx]
            signal_visual.set_max_signal_value(self.max_value)
            signal_visual.set_target_position((0, pos_y))
            signal_visual.draw(overlay_draw, self.font, self.current_date)
            pos_y += self.config.bar_height

        draw_text(draw,
                  text=self.current_date.strftime(self.config.date_format),
                  position=(self.config.margin, self.config.margin),
                  font=self.font,
                  fill_color=self.config.text_fill_color,
                  center_x=False,
                  center_y=False
                  )

        draw_text(draw,
                  text=self.config.video_title,
                  position=(self.config.image_size_x / 2, self.config.margin),
                  font=self.title_font,
                  fill_color=self.config.text_fill_color,
                  center_x=True,
                  center_y=False
                  )

        image = Image.alpha_composite(image, overlay)
        image.alpha_composite(self.logo_img, (self.config.image_size_x -
                                              300, self.config.image_size_y - 90))

        self.video_writer.write(cv2.cvtColor(
            np.array(image), cv2.COLOR_RGBA2BGR))

        self.start_frame_counter += 1

        if self.start_frame_counter >= self.config.start_frames:
            self.current_date += self.config.frame_time_interval

        if self.current_date >= self.config.end_date:
            self.end_frame_counter += 1
            if self.end_frame_counter >= self.config.end_frames:
                return False
            self.current_date = self.config.end_date  # reset

        return True
