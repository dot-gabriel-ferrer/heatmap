"""
Motion Module

This module provides functionality for updating point cloud coordinates,
useful for creating animated heatmaps.
"""

from typing import Union, Tuple
import numpy as np
from numpy.typing import NDArray


def update_coordinates(
    x: Union[NDArray, list],
    y: Union[NDArray, list],
    x_delta: Union[NDArray, list, float],
    y_delta: Union[NDArray, list, float]
) -> Tuple[NDArray, NDArray]:
    """
    Update coordinates by adding delta values.
    
    This function is useful for simulating motion in point cloud data,
    enabling the creation of animated heatmaps.
    
    Args:
        x: Current X coordinates
        y: Current Y coordinates
        x_delta: Delta values to add to X coordinates
        y_delta: Delta values to add to Y coordinates
        
    Returns:
        Tuple of (updated_x, updated_y) as numpy arrays
    """
    updated_x = np.asarray(x) + np.asarray(x_delta)
    updated_y = np.asarray(y) + np.asarray(y_delta)
    
    return updated_x, updated_y
