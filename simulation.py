"""
Heatmap Animation Simulation

This script demonstrates how to create an animated heatmap by simulating
moving point cloud data over time.
"""

import random
import numpy as np

from motion.motion import update_coordinates
from heatmap.heatmap_generator import create_heatmap_from_points
from animation.images import overlay_images


def main():
    """Generate animated heatmap simulation."""
    # Create random initial coordinates
    x = np.random.randint(0, 100, 100)
    y = np.random.randint(0, 100, 100)
    
    # Generate frames
    num_frames = 500
    for i in range(num_frames):
        # Random direction signs
        x_sign = random.choice([1, -1])
        y_sign = random.choice([1, -1])
        
        # Generate heatmap for current positions
        frame_path = f"output/frame{i}.png"
        create_heatmap_from_points(frame_path, x, y)
        
        # Calculate random movement
        x_delta = np.random.random(100) * x_sign
        y_delta = np.random.random(100) * y_sign
        
        # Update coordinates
        x, y = update_coordinates(x, y, x_delta, y_delta)
        
        # Overlay heatmap on background
        overlay_images("background.png", frame_path, frame_path)


if __name__ == "__main__":
    main()

