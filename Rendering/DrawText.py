"""    
This file is part of VideoBeam.

VideoBeam is created by Marius Fabry.
"""

import cv2
from PIL import ImageDraw


def draw_text(pil_image_draw, text, position, font, fill_color, center_x=True, center_y=True):
    pos = position
    size = pil_image_draw.textsize(text, font=font)
    if center_x:
        pos = (pos[0] - int(size[0] / 2), pos[1])
    if center_y:
        pos = (pos[0], pos[1] - int(size[1] / 2))
    pil_image_draw.text(pos, text, fill_color, font=font)
