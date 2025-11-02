"""
Animation Example

This example demonstrates how to create an animated heatmap showing
temporal changes in point cloud data.
"""

import numpy as np
from pathlib import Path

from heatmap.heatmap_generator import create_heatmap_from_points
from animation.togif import create_gif
from motion.motion import update_coordinates


def main():
    """Create an animated heatmap."""
    # Create output directory
    frames_dir = Path('examples/frames')
    frames_dir.mkdir(exist_ok=True)
    
    # Initialize point cloud with clusters
    np.random.seed(42)
    
    # Create three clusters of points
    cluster1_x = np.random.normal(30, 5, 30)
    cluster1_y = np.random.normal(30, 5, 30)
    
    cluster2_x = np.random.normal(70, 5, 30)
    cluster2_y = np.random.normal(70, 5, 30)
    
    cluster3_x = np.random.normal(50, 5, 40)
    cluster3_y = np.random.normal(50, 5, 40)
    
    x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
    y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])
    
    # Generate animation frames
    num_frames = 50
    print(f"Generating {num_frames} frames...")
    
    for i in range(num_frames):
        frame_path = frames_dir / f'frame_{i:03d}.png'
        
        # Generate heatmap for current positions
        create_heatmap_from_points(
            str(frame_path),
            x, y,
            grid_size=2.0,
            bandwidth=10.0,
            colormap='plasma'
        )
        
        # Update positions with some random motion
        x_delta = np.random.randn(len(x)) * 0.5
        y_delta = np.random.randn(len(y)) * 0.5
        x, y = update_coordinates(x, y, x_delta, y_delta)
        
        if (i + 1) % 10 == 0:
            print(f"Generated {i + 1}/{num_frames} frames")
    
    # Create GIF
    print("Creating GIF animation...")
    create_gif(
        str(frames_dir / 'frame_*.png'),
        'examples/animation.gif',
        duration=100,
        loop=0,
        quality=75
    )
    
    print("Animation saved to examples/animation.gif")
    
    # Cleanup frames
    import shutil
    shutil.rmtree(frames_dir)
    print("Cleaned up temporary frames")


if __name__ == '__main__':
    main()
