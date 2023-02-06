import matplotlib.pyplot as plt
import numpy as np
import math
import json

# function to read json file and return x and y coordinates
def get_coordinates(json_file):
    with open(json_file) as f:
        data = json.load(f)
    x = []
    y = []
    for i in data:
        x.append(i['x'])
        y.append(i['y'])
    return x, y

#FUNCTION TO CALCULATE INTENSITY WITH QUARTIC KERNEL
def kde_quartic(d,h):
    dn=d/h
    P=(1)*(1-dn**2)**2
    return P

# function to generate meshgrid
def meshgrid(x, y, grid_size, h):
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    x_grid = np.arange(x_min - h, x_max + h, grid_size)
    y_grid = np.arange(y_min - h, y_max + h, grid_size)
    x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)
    xc = x_mesh + (grid_size / 2)
    yc = y_mesh + (grid_size / 2)
    return xc, yc, x_mesh, y_mesh

# function to process data
def process_data(x, y, xc, yc, h):
    intensity_list = []
    for j in range(len(xc)):
        intensity_row = []
        for k in range(len(xc[0])):
            kde_value_list = []
            for i in range(len(x)):
                # CALCULATE DISTANCE
                d = math.sqrt((xc[j][k] - x[i]) ** 2 + (yc[j][k] - y[i]) ** 2)
                if d <= h:
                    p = kde_quartic(d, h)
                else:
                    p = 0
                kde_value_list.append(p)
            # SUM ALL INTENSITY VALUE
            p_total = sum(kde_value_list)
            intensity_row.append(p_total)
        intensity_list.append(intensity_row)
    intensity = np.array(intensity_list)
    return intensity

# function to generate alpha clip
def alpha_clip(intensity):
    alpha_clip = (intensity - intensity.min()) / (intensity.max() - intensity.min())
    return alpha_clip

# function to output heatmap
def heatmap_output(name, x_mesh, y_mesh, intensity, alpha_clip):
    fig, ax = plt.subplots()
    # smooth the heatmap
    ax.imshow(intensity, cmap='gist_heat', interpolation='gaussian', alpha=alpha_clip)
    # set initial coordinates of the heatmap as 0,0 at bottom left
    ax.set_xlim(0, len(x_mesh))
    ax.set_ylim(0, len(y_mesh))

    #ax.pcolormesh(x_mesh,y_mesh,intensity, alpha=intensity_norm, cmap='gist_heat')
    ax.axis('off')
    ax.set_aspect('equal')
    # remove white border
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(name, transparent = True)

# function to create heatmap
def create_heatmap(name, json_file, grid_size=1, h=10):
    x, y = get_coordinates(json_file)
    xc, yc, x_mesh, y_mesh = meshgrid(x, y, grid_size, h)
    intensity = process_data(x, y, xc, yc, h)
    alpha = alpha_clip(intensity)
    heatmap_output(name, x_mesh, y_mesh, intensity, alpha)

# function to create heatmap with random x and y coordinates
def create_heatmap_random(name, x, y, grid_size=10, h=10):
    xc, yc, x_mesh, y_mesh = meshgrid(x, y, grid_size, h)
    intensity = process_data(x, y, xc, yc, h)
    alpha = alpha_clip(intensity)
    heatmap_output(name, x_mesh, y_mesh, intensity, alpha)

# example of using the function to create heatmap randomly
#x = [30,26,23,65,52,45,55,75]
#y = [5,20,35,30,30,55,75,100]
#create_heatmap_random("random",x, y)

