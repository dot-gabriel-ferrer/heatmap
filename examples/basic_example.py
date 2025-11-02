"""
Basic Heatmap Example

This example demonstrates how to create a simple heatmap from point cloud data.
"""

import numpy as np
from heatmap.heatmap_generator import create_heatmap_from_points


def main():
    """Generate a basic heatmap from random point cloud data."""
    # Generate random point cloud data
    np.random.seed(42)  # For reproducibility
    x = np.random.rand(100) * 100
    y = np.random.rand(100) * 100
    
    # Create heatmap
    print("Generating heatmap...")
    create_heatmap_from_points(
        output_path='examples/basic_heatmap.png',
        x=x,
        y=y,
        grid_size=2.0,
        bandwidth=15.0,
        colormap='hot'
    )
    print("Heatmap saved to examples/basic_heatmap.png")


if __name__ == '__main__':
    main()
