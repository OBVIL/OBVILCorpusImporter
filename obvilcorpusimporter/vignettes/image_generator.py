#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
image_generator.py is part of the project OBVILCorpusImporter
Author: Valérie Hanoka

"""
import os
from PIL import ImageFont, Image, ImageDraw
import textwrap

# Fonts
this_dir = os.path.dirname(os.path.realpath(__file__))
BOLD = ImageFont.truetype("%s/font/Crimson_Text/CrimsonText-SemiBold.ttf" % this_dir, 60)
NORMAL = ImageFont.truetype("%s/font/Crimson_Text/CrimsonText-Regular.ttf" % this_dir, 40)

# Logo location
LOGO = '%s/img/logo_minimalist.png' % this_dir

# Layout
H_SPACE = 10
BIG_H_SPACE = 20 * H_SPACE
V_SPACE = 10
interline = 5

BACKGROUND_COLOR = (255, 255, 255, 255)
TEXT_COLOR = (0, 0, 0)

# Image size
MAX_W, MAX_H = 1000, 1000

def create_image(identifier, title, author, save_in_folder='.'):
    background = Image.new('RGBA', (MAX_W, MAX_H), BACKGROUND_COLOR)

    # Adding the OBVIL logo to it
    logo = Image.open(LOGO, 'r')
    logo_w, logo_h = logo.size
    bg_w, bg_h = background.size
    background.paste(logo, ((bg_w//2) - (logo_w//2), 5 * H_SPACE))
    draw = ImageDraw.Draw(background)

    end_of_logo = logo_h + BIG_H_SPACE

    # Title
    para_title = textwrap.wrap(title, width=40)
    current_h, pad = end_of_logo, interline
    for line in para_title:
        w, h = draw.textsize(line, font=BOLD)
        draw.text(((MAX_W - w) / 2, current_h), line, TEXT_COLOR, font=BOLD)
        current_h += h + pad

    # Author
    para_author = textwrap.wrap(author, width=40)
    current_h, pad = current_h + BIG_H_SPACE, pad
    for line in para_author:
        w, h = draw.textsize(line, font=NORMAL)
        draw.text(((MAX_W - w) / 2, current_h), line, TEXT_COLOR, font=NORMAL)
        current_h += h + pad

    background.save("%s/%s.png" % (save_in_folder.strip('/'), identifier))
