"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

from DataSources.Signal import Signal
from Rendering.DrawText import draw_text


class SignalVisual:
    def __init__(self, signal, render_config):
        self.signal = signal
        self.config = render_config
        self.position = [0, render_config.image_size_y * 1.5]
        self.target_position = [0, 0]
        self.move_factor = 0.06
        self.max_signal_value = 1.0

    def draw(self, draw, font, date):
        self._update_position()

        pos_y = self.position[1]

        key = self.signal.get_name()
        value = self.signal.get_value(date)
        right_bar_end_pos = self.config.margin + self.config.left_image_margin + value / self.max_signal_value * \
            (self.config.image_size_x - self.config.margin -
                self.config.right_image_margin - self.config.left_image_margin)
        draw.rectangle([(self.config.margin + self.config.left_image_margin, pos_y+self.config.margin),
                        (right_bar_end_pos, pos_y + self.config.bar_height - self.config.margin)], fill=self.config.rectangle_fill_color)
        text_pos_y = pos_y + self.config.bar_height / 2

        draw_text(pil_image_draw=draw,
                  text=str(key),
                  position=(self.config.margin, text_pos_y),
                  font=font,
                  fill_color=self.config.text_fill_color,
                  center_x=False,
                  center_y=True)

        if value < 100:
            value_str = "{:.2f}".format(value)
        else:
            value_str = str(int(value))

        draw_text(pil_image_draw=draw,
                  text=value_str + self.signal.get_unit(),
                  position=(right_bar_end_pos + 2 *
                            self.config.margin, text_pos_y),
                  font=font,
                  fill_color=self.config.text_fill_color,
                  center_x=False,
                  center_y=True)

    def set_target_position(self, target_position):
        self.target_position = target_position

    def set_position(self, position):
        self.position = position

    def set_max_signal_value(self, value):
        self.max_signal_value = value

    def _update_position(self):
        self.position[0] += (self.target_position[0] -
                             self.position[0]) * self.move_factor
        self.position[1] += (self.target_position[1] -
                             self.position[1]) * self.move_factor
