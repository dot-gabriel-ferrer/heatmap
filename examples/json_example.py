"""
JSON Data Example

This example demonstrates how to create a heatmap from JSON coordinate data.
"""

from heatmap.heatmap_generator import create_heatmap


def main():
    """Generate a heatmap from JSON data file."""
    print("Generating heatmap from JSON data...")
    create_heatmap(
        output_path='examples/json_heatmap.png',
        json_file='examples/sample_data.json',
        grid_size=1.0,
        bandwidth=10.0,
        colormap='viridis',
        interpolation='gaussian'
    )
    print("Heatmap saved to examples/json_heatmap.png")


if __name__ == '__main__':
    main()
