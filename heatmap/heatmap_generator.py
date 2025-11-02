"""
Heatmap Generator Module

This module provides functionality for generating heatmaps using Kernel Density
Estimation (KDE) with a quartic kernel. It supports both point cloud data and
JSON-based coordinate input.
"""

import json
import logging
import math
from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

# Get logger for this module
logger = logging.getLogger(__name__)


def get_coordinates(json_file: str) -> Tuple[List[float], List[float]]:
    """
    Read coordinates from a JSON file.
    
    Args:
        json_file: Path to JSON file containing coordinates with 'x' and 'y' keys
        
    Returns:
        Tuple of (x_coordinates, y_coordinates) as lists
        
    Raises:
        FileNotFoundError: If the JSON file does not exist
        json.JSONDecodeError: If the JSON file is malformed
        KeyError: If required keys are missing from JSON data
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        x = []
        y = []
        for point in data:
            x.append(point['x'])
            y.append(point['y'])
        
        logger.info(f"Loaded {len(x)} coordinates from {json_file}")
        return x, y
    
    except FileNotFoundError:
        logger.error(f"File not found: {json_file}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {json_file}: {e}")
        raise
    except KeyError as e:
        logger.error(f"Missing required key in JSON data: {e}")
        raise


def kde_quartic(distance: float, bandwidth: float) -> float:
    """
    Calculate intensity using quartic kernel for Kernel Density Estimation.
    
    The quartic kernel is defined as: K(u) = (1 - u^2)^2 for |u| <= 1
    
    Args:
        distance: Distance from the point
        bandwidth: Bandwidth parameter (smoothing parameter)
        
    Returns:
        Kernel density value
    """
    normalized_distance = distance / bandwidth
    kernel_value = (1 - normalized_distance ** 2) ** 2
    return kernel_value


def create_meshgrid(
    x: Union[List[float], NDArray],
    y: Union[List[float], NDArray],
    grid_size: float,
    bandwidth: float
) -> Tuple[NDArray, NDArray, NDArray, NDArray]:
    """
    Generate a meshgrid for heatmap calculation.
    
    Args:
        x: X coordinates of data points
        y: Y coordinates of data points
        grid_size: Size of grid cells
        bandwidth: Bandwidth parameter for extending grid boundaries
        
    Returns:
        Tuple of (xc, yc, x_mesh, y_mesh) where:
            - xc, yc: Center coordinates of grid cells
            - x_mesh, y_mesh: Meshgrid arrays
    """
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    
    x_grid = np.arange(x_min - bandwidth, x_max + bandwidth, grid_size)
    y_grid = np.arange(y_min - bandwidth, y_max + bandwidth, grid_size)
    x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)
    
    xc = x_mesh + (grid_size / 2)
    yc = y_mesh + (grid_size / 2)
    
    return xc, yc, x_mesh, y_mesh


def calculate_intensity(
    x: Union[List[float], NDArray],
    y: Union[List[float], NDArray],
    xc: NDArray,
    yc: NDArray,
    bandwidth: float
) -> NDArray:
    """
    Calculate intensity values for heatmap using KDE.
    
    Args:
        x: X coordinates of data points
        y: Y coordinates of data points
        xc: X coordinates of grid cell centers
        yc: Y coordinates of grid cell centers
        bandwidth: Bandwidth parameter for KDE
        
    Returns:
        2D numpy array of intensity values
    """
    intensity_list = []
    
    for j in range(len(xc)):
        intensity_row = []
        for k in range(len(xc[0])):
            kde_values = []
            
            for i in range(len(x)):
                # Calculate Euclidean distance
                distance = math.sqrt((xc[j][k] - x[i]) ** 2 + (yc[j][k] - y[i]) ** 2)
                
                if distance <= bandwidth:
                    kde_value = kde_quartic(distance, bandwidth)
                else:
                    kde_value = 0
                
                kde_values.append(kde_value)
            
            # Sum all intensity values for this grid cell
            total_intensity = sum(kde_values)
            intensity_row.append(total_intensity)
        
        intensity_list.append(intensity_row)
    
    intensity = np.array(intensity_list)
    logger.info(f"Calculated intensity matrix of shape {intensity.shape}")
    
    return intensity


def normalize_alpha(intensity: NDArray) -> NDArray:
    """
    Normalize intensity values to [0, 1] range for alpha channel.
    
    Args:
        intensity: 2D array of intensity values
        
    Returns:
        Normalized intensity values
    """
    if intensity.max() == intensity.min():
        logger.warning("Constant intensity values detected, returning zeros")
        return np.zeros_like(intensity)
    
    normalized = (intensity - intensity.min()) / (intensity.max() - intensity.min())
    return normalized


def save_heatmap(
    output_path: str,
    x_mesh: NDArray,
    y_mesh: NDArray,
    intensity: NDArray,
    alpha: NDArray,
    colormap: str = 'jet',
    interpolation: str = 'gaussian'
) -> None:
    """
    Save heatmap visualization to file.
    
    Args:
        output_path: Path to save the heatmap image
        x_mesh: X coordinates meshgrid
        y_mesh: Y coordinates meshgrid
        intensity: Intensity values
        alpha: Alpha channel values
        colormap: Matplotlib colormap name (default: 'jet')
        interpolation: Interpolation method (default: 'gaussian')
    """
    fig, ax = plt.subplots()
    
    ax.imshow(intensity, cmap=colormap, interpolation=interpolation, alpha=alpha)
    ax.set_xlim(0, len(x_mesh))
    ax.set_ylim(0, len(y_mesh))
    ax.axis('off')
    ax.set_aspect('equal')
    
    # Remove white border
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(output_path, transparent=True)
    plt.close(fig)
    
    logger.info(f"Heatmap saved to {output_path}")


def create_heatmap(
    output_path: str,
    json_file: str,
    grid_size: float = 1.0,
    bandwidth: float = 10.0,
    colormap: str = 'jet',
    interpolation: str = 'gaussian'
) -> None:
    """
    Create a heatmap from JSON coordinate data.
    
    Args:
        output_path: Path to save the output heatmap image
        json_file: Path to JSON file with coordinate data
        grid_size: Size of grid cells (default: 1.0)
        bandwidth: Bandwidth parameter for KDE (default: 10.0)
        colormap: Matplotlib colormap name (default: 'jet')
        interpolation: Interpolation method (default: 'gaussian')
    """
    x, y = get_coordinates(json_file)
    xc, yc, x_mesh, y_mesh = create_meshgrid(x, y, grid_size, bandwidth)
    intensity = calculate_intensity(x, y, xc, yc, bandwidth)
    alpha = normalize_alpha(intensity)
    save_heatmap(output_path, x_mesh, y_mesh, intensity, alpha, colormap, interpolation)


def create_heatmap_from_points(
    output_path: str,
    x: Union[List[float], NDArray],
    y: Union[List[float], NDArray],
    grid_size: float = 10.0,
    bandwidth: float = 10.0,
    colormap: str = 'jet',
    interpolation: str = 'gaussian'
) -> None:
    """
    Create a heatmap from point cloud data.
    
    Args:
        output_path: Path to save the output heatmap image
        x: X coordinates of data points
        y: Y coordinates of data points
        grid_size: Size of grid cells (default: 10.0)
        bandwidth: Bandwidth parameter for KDE (default: 10.0)
        colormap: Matplotlib colormap name (default: 'jet')
        interpolation: Interpolation method (default: 'gaussian')
    """
    xc, yc, x_mesh, y_mesh = create_meshgrid(x, y, grid_size, bandwidth)
    intensity = calculate_intensity(x, y, xc, yc, bandwidth)
    alpha = normalize_alpha(intensity)
    save_heatmap(output_path, x_mesh, y_mesh, intensity, alpha, colormap, interpolation)
