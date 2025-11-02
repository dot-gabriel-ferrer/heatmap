# API Documentation

Complete API reference for the Heatmap Generator library.

## Table of Contents

- [heatmap.heatmap_generator](#heatmapheatmap_generator)
- [motion.motion](#motionmotion)
- [animation.images](#animationimages)
- [animation.togif](#animationtogif)
- [utils.image_utils](#utilsimage_utils)

---

## heatmap.heatmap_generator

Module for generating heatmaps using Kernel Density Estimation.

### Functions

#### `get_coordinates(json_file: str) -> Tuple[List[float], List[float]]`

Read coordinates from a JSON file.

**Parameters:**
- `json_file` (str): Path to JSON file containing coordinates with 'x' and 'y' keys

**Returns:**
- Tuple of (x_coordinates, y_coordinates) as lists

**Raises:**
- `FileNotFoundError`: If the JSON file does not exist
- `json.JSONDecodeError`: If the JSON file is malformed
- `KeyError`: If required keys are missing from JSON data

**Example:**
```python
x, y = get_coordinates('data.json')
```

---

#### `kde_quartic(distance: float, bandwidth: float) -> float`

Calculate intensity using quartic kernel for Kernel Density Estimation.

The quartic kernel is defined as: K(u) = (1 - u^2)^2 for |u| <= 1

**Parameters:**
- `distance` (float): Distance from the point
- `bandwidth` (float): Bandwidth parameter (smoothing parameter)

**Returns:**
- float: Kernel density value

**Example:**
```python
kernel_value = kde_quartic(5.0, 10.0)
```

---

#### `create_meshgrid(x, y, grid_size: float, bandwidth: float) -> Tuple[NDArray, NDArray, NDArray, NDArray]`

Generate a meshgrid for heatmap calculation.

**Parameters:**
- `x` (array-like): X coordinates of data points
- `y` (array-like): Y coordinates of data points
- `grid_size` (float): Size of grid cells
- `bandwidth` (float): Bandwidth parameter for extending grid boundaries

**Returns:**
- Tuple of (xc, yc, x_mesh, y_mesh) where:
  - xc, yc: Center coordinates of grid cells
  - x_mesh, y_mesh: Meshgrid arrays

**Example:**
```python
xc, yc, x_mesh, y_mesh = create_meshgrid(x, y, grid_size=1.0, bandwidth=10.0)
```

---

#### `calculate_intensity(x, y, xc, yc, bandwidth: float) -> NDArray`

Calculate intensity values for heatmap using KDE.

**Parameters:**
- `x` (array-like): X coordinates of data points
- `y` (array-like): Y coordinates of data points
- `xc` (NDArray): X coordinates of grid cell centers
- `yc` (NDArray): Y coordinates of grid cell centers
- `bandwidth` (float): Bandwidth parameter for KDE

**Returns:**
- NDArray: 2D numpy array of intensity values

**Example:**
```python
intensity = calculate_intensity(x, y, xc, yc, bandwidth=10.0)
```

---

#### `normalize_alpha(intensity: NDArray) -> NDArray`

Normalize intensity values to [0, 1] range for alpha channel.

**Parameters:**
- `intensity` (NDArray): 2D array of intensity values

**Returns:**
- NDArray: Normalized intensity values

**Example:**
```python
alpha = normalize_alpha(intensity)
```

---

#### `save_heatmap(output_path, x_mesh, y_mesh, intensity, alpha, colormap='jet', interpolation='gaussian')`

Save heatmap visualization to file.

**Parameters:**
- `output_path` (str): Path to save the heatmap image
- `x_mesh` (NDArray): X coordinates meshgrid
- `y_mesh` (NDArray): Y coordinates meshgrid
- `intensity` (NDArray): Intensity values
- `alpha` (NDArray): Alpha channel values
- `colormap` (str): Matplotlib colormap name (default: 'jet')
- `interpolation` (str): Interpolation method (default: 'gaussian')

**Example:**
```python
save_heatmap('output.png', x_mesh, y_mesh, intensity, alpha, colormap='viridis')
```

---

#### `create_heatmap(output_path, json_file, grid_size=1.0, bandwidth=10.0, colormap='jet', interpolation='gaussian')`

Create a heatmap from JSON coordinate data.

**Parameters:**
- `output_path` (str): Path to save the output heatmap image
- `json_file` (str): Path to JSON file with coordinate data
- `grid_size` (float): Size of grid cells (default: 1.0)
- `bandwidth` (float): Bandwidth parameter for KDE (default: 10.0)
- `colormap` (str): Matplotlib colormap name (default: 'jet')
- `interpolation` (str): Interpolation method (default: 'gaussian')

**Example:**
```python
create_heatmap('output.png', 'data.json', grid_size=2.0, bandwidth=15.0)
```

---

#### `create_heatmap_from_points(output_path, x, y, grid_size=10.0, bandwidth=10.0, colormap='jet', interpolation='gaussian')`

Create a heatmap from point cloud data.

**Parameters:**
- `output_path` (str): Path to save the output heatmap image
- `x` (array-like): X coordinates of data points
- `y` (array-like): Y coordinates of data points
- `grid_size` (float): Size of grid cells (default: 10.0)
- `bandwidth` (float): Bandwidth parameter for KDE (default: 10.0)
- `colormap` (str): Matplotlib colormap name (default: 'jet')
- `interpolation` (str): Interpolation method (default: 'gaussian')

**Example:**
```python
import numpy as np
x = np.random.rand(100) * 100
y = np.random.rand(100) * 100
create_heatmap_from_points('output.png', x, y, bandwidth=15.0)
```

---

## motion.motion

Module for updating point cloud coordinates.

### Functions

#### `update_coordinates(x, y, x_delta, y_delta) -> Tuple[NDArray, NDArray]`

Update point cloud coordinates by adding delta values.

**Parameters:**
- `x` (array-like): Current X coordinates
- `y` (array-like): Current Y coordinates
- `x_delta` (array-like or float): Change in X coordinates
- `y_delta` (array-like or float): Change in Y coordinates

**Returns:**
- Tuple of (updated_x, updated_y) as numpy arrays

**Example:**
```python
import numpy as np
x = np.array([1.0, 2.0, 3.0])
y = np.array([4.0, 5.0, 6.0])
x_delta = np.array([0.5, 0.5, 0.5])
y_delta = np.array([-0.5, -0.5, -0.5])
new_x, new_y = update_coordinates(x, y, x_delta, y_delta)
```

---

## animation.images

Module for image overlay operations.

### Functions

#### `overlay_images(background_path, overlay_path, output_path, crop_box=None)`

Overlay a transparent image onto a background image.

**Parameters:**
- `background_path` (str): Path to the background image
- `overlay_path` (str): Path to the overlay image (should have transparency)
- `output_path` (str): Path to save the composite image
- `crop_box` (tuple, optional): Tuple (left, top, right, bottom) for cropping the result

**Raises:**
- `FileNotFoundError`: If input images do not exist
- `IOError`: If there's an error reading or writing images

**Example:**
```python
overlay_images('map.png', 'heatmap.png', 'result.png', crop_box=(100, 100, 500, 500))
```

---

## animation.togif

Module for creating GIF animations.

### Functions

#### `create_gif(input_pattern, output_path, duration=20, loop=0, quality=50, optimize=False)`

Create an animated GIF from a sequence of images.

**Parameters:**
- `input_pattern` (str): Glob pattern for input images (e.g., "frames/frame*.png")
- `output_path` (str): Path to save the output GIF
- `duration` (int): Duration of each frame in milliseconds (default: 20)
- `loop` (int): Number of times to loop the animation, 0 for infinite (default: 0)
- `quality` (int): JPEG quality for GIF compression, 1-100 (default: 50)
- `optimize` (bool): Whether to optimize the GIF palette (default: False)

**Raises:**
- `ValueError`: If no images match the input pattern
- `IOError`: If there's an error reading images or writing the GIF

**Example:**
```python
create_gif('frames/frame_*.png', 'animation.gif', duration=50, loop=0)
```

---

#### `create_gif_from_directory(input_dir, output_path, extension='png', duration=20, loop=0, quality=50, optimize=False)`

Create an animated GIF from all images in a directory.

**Parameters:**
- `input_dir` (str): Directory containing input images
- `output_path` (str): Path to save the output GIF
- `extension` (str): File extension to match (default: "png")
- `duration` (int): Duration of each frame in milliseconds (default: 20)
- `loop` (int): Number of times to loop the animation, 0 for infinite (default: 0)
- `quality` (int): JPEG quality for GIF compression, 1-100 (default: 50)
- `optimize` (bool): Whether to optimize the GIF palette (default: False)

**Example:**
```python
create_gif_from_directory('frames', 'animation.gif', extension='png', duration=100)
```

---

## utils.image_utils

Module for image utility functions.

### Functions

#### `crop_image(input_path, output_path, crop_box)`

Crop an image to a specified bounding box.

**Parameters:**
- `input_path` (str): Path to the input image
- `output_path` (str): Path to save the cropped image
- `crop_box` (tuple): Tuple of (left, top, right, bottom) coordinates

**Raises:**
- `FileNotFoundError`: If the input image does not exist
- `IOError`: If there's an error reading or writing the image

**Example:**
```python
crop_image('input.png', 'cropped.png', (100, 100, 400, 400))
```

---

#### `resize_image(input_path, output_path, size, maintain_aspect=True)`

Resize an image to specified dimensions.

**Parameters:**
- `input_path` (str): Path to the input image
- `output_path` (str): Path to save the resized image
- `size` (tuple): Tuple of (width, height) for the new size
- `maintain_aspect` (bool): If True, maintains aspect ratio using thumbnail method

**Raises:**
- `FileNotFoundError`: If the input image does not exist
- `IOError`: If there's an error reading or writing the image

**Example:**
```python
resize_image('large.png', 'small.png', (800, 600), maintain_aspect=True)
```
