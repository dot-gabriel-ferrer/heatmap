# User Guide

This guide provides detailed instructions for using the Heatmap Generator.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Command Line Interface](#command-line-interface)
4. [Python API](#python-api)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

## Installation

### Requirements

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

The following packages will be installed:
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- Pillow >= 10.0.0

### Verify Installation

```bash
python cli.py --help
```

## Quick Start

### Generate Your First Heatmap

1. Create a JSON file with coordinate data:

```json
[
    {"x": 10, "y": 20},
    {"x": 15, "y": 25},
    {"x": 20, "y": 30}
]
```

2. Generate the heatmap:

```bash
python cli.py generate --input data.json --output heatmap.png
```

3. View the output image `heatmap.png`

### Run an Example

```bash
python examples/basic_example.py
```

## Command Line Interface

The CLI provides four main commands:

### 1. Generate Command

Create a heatmap from JSON data.

```bash
python cli.py generate --input data.json --output heatmap.png [options]
```

**Options:**
- `--grid-size`: Size of grid cells (default: 1.0)
- `--bandwidth`: KDE bandwidth parameter (default: 10.0)
- `--colormap`: Matplotlib colormap (default: jet)
- `--interpolation`: Interpolation method (default: gaussian)

**Example:**
```bash
python cli.py generate \
    --input coordinates.json \
    --output result.png \
    --grid-size 2.0 \
    --bandwidth 15.0 \
    --colormap viridis
```

### 2. Animate Command

Create an animated heatmap.

```bash
python cli.py animate --output animation.gif [options]
```

**Options:**
- `--frames`: Number of frames (default: 100)
- `--points`: Number of points (default: 100)
- `--background`: Background image path (optional)
- `--duration`: Frame duration in ms (default: 20)
- `--grid-size`: Grid cell size (default: 10.0)
- `--bandwidth`: KDE bandwidth (default: 10.0)

**Example:**
```bash
python cli.py animate \
    --frames 200 \
    --output animation.gif \
    --background map.png \
    --duration 30
```

### 3. Overlay Command

Overlay a heatmap on a background image.

```bash
python cli.py overlay \
    --background map.png \
    --heatmap heat.png \
    --output result.png \
    [--crop left,top,right,bottom]
```

**Example:**
```bash
python cli.py overlay \
    --background city_map.png \
    --heatmap density.png \
    --output final.png \
    --crop 100,100,500,500
```

### 4. GIF Command

Create a GIF from an image sequence.

```bash
python cli.py gif --input "frames/*.png" --output animation.gif [options]
```

**Options:**
- `--duration`: Frame duration in ms (default: 20)
- `--loop`: Number of loops, 0 for infinite (default: 0)
- `--quality`: Quality 1-100 (default: 50)
- `--optimize`: Enable palette optimization (flag)

**Example:**
```bash
python cli.py gif \
    --input "frames/frame_*.png" \
    --output result.gif \
    --duration 50 \
    --quality 75 \
    --optimize
```

## Python API

### Basic Heatmap

```python
import numpy as np
from heatmap.heatmap_generator import create_heatmap_from_points

# Generate random data
x = np.random.rand(100) * 100
y = np.random.rand(100) * 100

# Create heatmap
create_heatmap_from_points(
    output_path='heatmap.png',
    x=x,
    y=y,
    grid_size=2.0,
    bandwidth=15.0,
    colormap='hot'
)
```

### Heatmap from JSON

```python
from heatmap.heatmap_generator import create_heatmap

create_heatmap(
    output_path='output.png',
    json_file='coordinates.json',
    grid_size=1.0,
    bandwidth=10.0
)
```

### Animated Heatmap

```python
import numpy as np
from motion.motion import update_coordinates
from heatmap.heatmap_generator import create_heatmap_from_points
from animation.togif import create_gif

# Initialize
x = np.random.rand(100) * 100
y = np.random.rand(100) * 100

# Generate frames
for i in range(50):
    create_heatmap_from_points(f'frame_{i:03d}.png', x, y)
    
    # Update positions
    x_delta = np.random.randn(100) * 2
    y_delta = np.random.randn(100) * 2
    x, y = update_coordinates(x, y, x_delta, y_delta)

# Create GIF
create_gif('frame_*.png', 'animation.gif', duration=50)
```

### Image Overlay

```python
from animation.images import overlay_images

overlay_images(
    background_path='map.png',
    overlay_path='heatmap.png',
    output_path='composite.png',
    crop_box=(100, 100, 500, 500)
)
```

## Advanced Usage

### Custom Color Maps

Matplotlib provides many color maps:

```python
# Hot colors
colormap='hot'        # Black → Red → Yellow → White
colormap='inferno'    # Black → Purple → Orange → Yellow

# Cool colors
colormap='cool'       # Cyan → Magenta
colormap='winter'     # Blue → Green

# Perceptually uniform
colormap='viridis'    # Purple → Green → Yellow
colormap='plasma'     # Purple → Pink → Yellow

# Diverging
colormap='coolwarm'   # Blue → White → Red
colormap='seismic'    # Blue → White → Red
```

### Bandwidth Selection

The bandwidth parameter controls smoothness:

- **Small bandwidth (5-10)**: Shows fine details, more granular
- **Medium bandwidth (10-20)**: Balanced visualization
- **Large bandwidth (20-50)**: Very smooth, broader patterns

```python
# Sharp details
create_heatmap_from_points('sharp.png', x, y, bandwidth=5)

# Smooth visualization
create_heatmap_from_points('smooth.png', x, y, bandwidth=30)
```

### Grid Size

Grid size affects resolution:

- **Small grid (0.5-1.0)**: High resolution, slower
- **Medium grid (1.0-5.0)**: Balanced
- **Large grid (5.0-10.0)**: Fast, lower resolution

```python
# High resolution
create_heatmap_from_points('hires.png', x, y, grid_size=0.5)

# Fast rendering
create_heatmap_from_points('fast.png', x, y, grid_size=10.0)
```

### Interpolation Methods

Available interpolation methods:

```python
interpolation='none'      # No interpolation (pixelated)
interpolation='bilinear'  # Bilinear interpolation
interpolation='gaussian'  # Gaussian smoothing (default)
interpolation='bicubic'   # Bicubic interpolation
```

### Working with Large Datasets

For large point clouds:

```python
# Use larger grid size for performance
create_heatmap_from_points(
    'large_dataset.png',
    x, y,
    grid_size=5.0,      # Larger grid
    bandwidth=20.0       # Compensate with larger bandwidth
)
```

## Troubleshooting

### Common Issues

#### Out of Memory

**Problem:** Program crashes with large datasets

**Solution:**
- Increase grid size
- Process data in chunks
- Reduce bandwidth

#### Heatmap Too Sparse

**Problem:** Points are barely visible

**Solution:**
- Increase bandwidth
- Decrease grid size
- Check data range

#### Heatmap Too Smooth

**Problem:** All details are blurred

**Solution:**
- Decrease bandwidth
- Increase grid size

#### File Not Found Error

**Problem:** Cannot find input files

**Solution:**
- Use absolute paths
- Check file permissions
- Verify file exists

#### Import Errors

**Problem:** ModuleNotFoundError

**Solution:**
```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/heatmap:$PYTHONPATH

# Or install in development mode
pip install -e .
```

### Getting Help

- Check the [API documentation](API.md)
- Review [examples](../examples/)
- Open an issue on GitHub
- Read the [CONTRIBUTING guide](../CONTRIBUTING.md)

## Best Practices

1. **Start Simple**: Begin with default parameters and adjust
2. **Test Small**: Use small datasets for testing
3. **Save Intermediate Results**: Keep intermediate outputs
4. **Use Appropriate Formats**: PNG for heatmaps, GIF for animations
5. **Document Parameters**: Keep track of settings that work well

## Performance Tips

1. Use appropriate grid size for your data scale
2. Process animations in batches
3. Use optimized GIF creation for large animations
4. Consider downsampling very large datasets
5. Use appropriate image formats (PNG is lossless)

## Next Steps

- Explore [examples](../examples/)
- Read the [API documentation](API.md)
- Check out [CHANGELOG](../CHANGELOG.md) for recent updates
- Contribute improvements (see [CONTRIBUTING](../CONTRIBUTING.md))
