"""
Unit tests for motion module.
"""

import unittest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

from motion.motion import update_coordinates


class TestUpdateCoordinates(unittest.TestCase):
    """Test coordinate update function."""
    
    def test_update_coordinates_lists(self):
        """Test updating coordinates with lists."""
        x = [1, 2, 3]
        y = [4, 5, 6]
        x_delta = [0.5, 1.0, 1.5]
        y_delta = [0.1, 0.2, 0.3]
        
        new_x, new_y = update_coordinates(x, y, x_delta, y_delta)
        
        expected_x = np.array([1.5, 3.0, 4.5])
        expected_y = np.array([4.1, 5.2, 6.3])
        
        assert_array_almost_equal(new_x, expected_x)
        assert_array_almost_equal(new_y, expected_y)
    
    def test_update_coordinates_arrays(self):
        """Test updating coordinates with numpy arrays."""
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([4.0, 5.0, 6.0])
        x_delta = np.array([1.0, 1.0, 1.0])
        y_delta = np.array([-1.0, -1.0, -1.0])
        
        new_x, new_y = update_coordinates(x, y, x_delta, y_delta)
        
        expected_x = np.array([2.0, 3.0, 4.0])
        expected_y = np.array([3.0, 4.0, 5.0])
        
        assert_array_almost_equal(new_x, expected_x)
        assert_array_almost_equal(new_y, expected_y)
    
    def test_update_coordinates_scalar_delta(self):
        """Test updating coordinates with scalar delta."""
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([4.0, 5.0, 6.0])
        x_delta = 5.0
        y_delta = -2.0
        
        new_x, new_y = update_coordinates(x, y, x_delta, y_delta)
        
        expected_x = np.array([6.0, 7.0, 8.0])
        expected_y = np.array([2.0, 3.0, 4.0])
        
        assert_array_almost_equal(new_x, expected_x)
        assert_array_almost_equal(new_y, expected_y)
    
    def test_update_coordinates_zero_delta(self):
        """Test updating coordinates with zero delta."""
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([4.0, 5.0, 6.0])
        x_delta = 0.0
        y_delta = 0.0
        
        new_x, new_y = update_coordinates(x, y, x_delta, y_delta)
        
        assert_array_almost_equal(new_x, x)
        assert_array_almost_equal(new_y, y)


if __name__ == '__main__':
    unittest.main()
