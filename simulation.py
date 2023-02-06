import motion.motion as m
import heatmap.heatmap_generator as h
import numpy as np
import animation.images as img

# create random values for x and y
x = np.random.randint(0, 100, 100)
y = np.random.randint(0, 100, 100)


for i in range(120):
    h.create_heatmap_random("output/frame" + str(i) + '.png', x, y)
    x_change = np.random.randint(-5, 5, 100)
    y_change = np.random.randint(-5, 5, 100)
    x, y = m.change_coordinates(x, y, x_change, y_change)
    img.overlap_images("background.png", "output/frame" + str(i) + '.png', "output/frame" + str(i) + '.png')