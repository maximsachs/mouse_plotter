#!/usr/bin/env python3
from get_draw_area import get_draw_area
import time
import PIL
import pprint
import os
import random
from PIL import Image
print('Pillow Version:', PIL.__version__)
from pymouse import PyMouse
import numpy as np
# from pykeyboard import PyKeyboard
m = PyMouse()
sleep_time = 0.05
draw_border = False
brush_size_pixels = 3
randomize_draw_order = False
draw_mode = "lines" # dots, lines

print("Make sure to select brush size 2 in BBB.")

print("Select image:")
image_files = [ f for f in os.listdir("images") if "jpeg" in f or "jpg" in f or "png" in f ]
image_files.sort()
pprint.pprint(dict(zip(range(len(image_files)), image_files)), compact=True, width=110)
image_file = image_files[int(input("Enter image index: "))]

# First getting the area in which we should draw.
top_left, bottom_right = get_draw_area()
center =(int((top_left[0]+bottom_right[0])/2), int((top_left[1]+bottom_right[1])/2))
drawing_size = (bottom_right[0]-top_left[0], bottom_right[1]-top_left[1])
print("Drawing Size:", drawing_size)
print("Let go of the mouse!")
for countdown in range(2,0,-1):
    print(countdown, "...")
    time.sleep(1)

print("Starting to plot")
# Moving mouse to center
m.move(center[0], center[1])
# # Doing single click there
# m.click(center[0], center[1])
# Drawing a box around the drawing area:
if draw_border:
    m.move(top_left[0], top_left[1])
    time.sleep(sleep_time)
    m.drag(top_left[0], bottom_right[1])
    time.sleep(sleep_time)
    m.drag(bottom_right[0], bottom_right[1])
    time.sleep(sleep_time)
    m.drag(bottom_right[0], top_left[1])
    time.sleep(sleep_time)
    m.drag(top_left[0], top_left[1])
    time.sleep(sleep_time)

img = Image.open(image_file)
# Making image bw:
thresh = 200
fn = lambda x : 255 if x > thresh else 0
img = img.convert('L').point(fn, mode='1')
# img = img.convert('1') 
# summarize some details about the image
print("Image Size:", img.size)
# print(img.mode)
# show the img
# img.show()

wpercent = ((drawing_size[1]/brush_size_pixels)/float(img.size[0]))
hsize = int((float(img.size[0])*float(wpercent)))
img = img.resize((int(drawing_size[0]/brush_size_pixels),hsize), Image.ANTIALIAS)
img_array = np.array(img)

print(img_array.shape)

if draw_mode == "dots":
    if not randomize_draw_order:
        for y, row in enumerate(img_array):
            for x, white in enumerate(row):
                if not white:
                    m.click(top_left[0]+(x*brush_size_pixels), top_left[1]+(y*brush_size_pixels))
                    time.sleep(sleep_time)
    else:
        pixels_to_draw = []
        for y, row in enumerate(img_array):
            for x, white in enumerate(row):
                if not white:
                    pixels_to_draw.append((x,y))
        random.shuffle(pixels_to_draw)
        for (x, y) in pixels_to_draw:
            m.click(top_left[0]+(x*brush_size_pixels), top_left[1]+(y*brush_size_pixels))
            time.sleep(sleep_time)
elif draw_mode == "lines":
    for y, row in enumerate(img_array):
        line_start = False
        for x, white in enumerate(row):
            if not white and not line_start:
                line_start = x
            elif white and line_start:
                m.move(top_left[0]+(line_start*brush_size_pixels), top_left[1]+(y*brush_size_pixels))
                m.drag(top_left[0]+(x*brush_size_pixels), top_left[1]+(y*brush_size_pixels))
                time.sleep(sleep_time)
                line_start = False
