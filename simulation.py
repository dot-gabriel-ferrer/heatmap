import motion.motion as m
import heatmap.heatmap_generator as h
import numpy as np
import animation.images as img
import random as r
# create random values for x and y
x = np.random.randint(0, 100, 100)
y = np.random.randint(0, 100, 100)


for i in range(500):
    x_sign = r.choice([1,-1])
    y_sign = r.choice([1,-1])
    h.create_heatmap_random("output/frame" + str(i) + '.png', x, y)
    x_change = np.random.random(100)*x_sign
    y_change = np.random.random(100)*y_sign
    x, y = m.change_coordinates(x, y, x_change, y_change)
    img.overlap_images("background.png", "output/frame" + str(i) + '.png', "output/frame" + str(i) + '.png')
