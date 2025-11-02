"""
Unit tests for heatmap_generator module.
"""

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from numpy.testing import assert_array_almost_equal

from heatmap.heatmap_generator import (
    get_coordinates,
    kde_quartic,
    create_meshgrid,
    calculate_intensity,
    normalize_alpha,
    create_heatmap_from_points,
    create_heatmap
)


class TestKDEQuartic(unittest.TestCase):
    """Test the quartic kernel function."""
    
    def test_kde_quartic_at_zero(self):
        """Test kernel value at zero distance."""
        result = kde_quartic(0, 10)
        self.assertEqual(result, 1.0)
    
    def test_kde_quartic_at_bandwidth(self):
        """Test kernel value at bandwidth distance."""
        result = kde_quartic(10, 10)
        self.assertEqual(result, 0.0)
    
    def test_kde_quartic_halfway(self):
        """Test kernel value at half bandwidth."""
        result = kde_quartic(5, 10)
        expected = (1 - 0.5**2)**2
        self.assertAlmostEqual(result, expected)


class TestGetCoordinates(unittest.TestCase):
    """Test coordinate loading from JSON."""
    
    def test_get_coordinates_valid_file(self):
        """Test loading coordinates from valid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([
                {"x": 1.0, "y": 2.0},
                {"x": 3.0, "y": 4.0}
            ], f)
            temp_path = f.name
        
        try:
            x, y = get_coordinates(temp_path)
            self.assertEqual(x, [1.0, 3.0])
            self.assertEqual(y, [2.0, 4.0])
        finally:
            Path(temp_path).unlink()
    
    def test_get_coordinates_missing_file(self):
        """Test error handling for missing file."""
        with self.assertRaises(FileNotFoundError):
            get_coordinates('nonexistent_file.json')


class TestCreateMeshgrid(unittest.TestCase):
    """Test meshgrid creation."""
    
    def test_create_meshgrid_simple(self):
        """Test basic meshgrid creation."""
        x = [0, 10]
        y = [0, 10]
        grid_size = 5
        bandwidth = 0
        
        xc, yc, x_mesh, y_mesh = create_meshgrid(x, y, grid_size, bandwidth)
        
        # Check that meshgrid was created
        self.assertIsInstance(xc, np.ndarray)
        self.assertIsInstance(yc, np.ndarray)
        self.assertEqual(xc.shape, yc.shape)


class TestCalculateIntensity(unittest.TestCase):
    """Test intensity calculation."""
    
    def test_calculate_intensity_single_point(self):
        """Test intensity with a single point."""
        x = [50]
        y = [50]
        
        # Create a small meshgrid
        xc = np.array([[45, 50, 55]])
        yc = np.array([[45, 50, 55]])
        
        intensity = calculate_intensity(x, y, xc, yc, bandwidth=10)
        
        # Intensity should be highest at the point location
        self.assertIsInstance(intensity, np.ndarray)
        self.assertEqual(intensity.shape, (1, 3))


class TestNormalizeAlpha(unittest.TestCase):
    """Test alpha normalization."""
    
    def test_normalize_alpha_range(self):
        """Test that normalization produces [0, 1] range."""
        intensity = np.array([[0, 5, 10], [2, 8, 6]])
        alpha = normalize_alpha(intensity)
        
        self.assertAlmostEqual(alpha.min(), 0.0)
        self.assertAlmostEqual(alpha.max(), 1.0)
    
    def test_normalize_alpha_constant(self):
        """Test normalization with constant values."""
        intensity = np.array([[5, 5], [5, 5]])
        alpha = normalize_alpha(intensity)
        
        # All values should be zero when input is constant
        assert_array_almost_equal(alpha, np.zeros_like(intensity))


class TestCreateHeatmapFromPoints(unittest.TestCase):
    """Test heatmap creation from points."""
    
    def test_create_heatmap_from_points(self):
        """Test creating heatmap from point data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_heatmap.png"
            
            x = np.array([10, 20, 30])
            y = np.array([10, 20, 30])
            
            create_heatmap_from_points(
                str(output_path),
                x, y,
                grid_size=5,
                bandwidth=10
            )
            
            # Check that output file was created
            self.assertTrue(output_path.exists())


class TestCreateHeatmap(unittest.TestCase):
    """Test heatmap creation from JSON."""
    
    def test_create_heatmap_from_json(self):
        """Test creating heatmap from JSON file."""
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([
                {"x": 10, "y": 10},
                {"x": 20, "y": 20},
                {"x": 30, "y": 30}
            ], f)
            json_path = f.name
        
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "test_heatmap.png"
                
                create_heatmap(
                    str(output_path),
                    json_path,
                    grid_size=5,
                    bandwidth=10
                )
                
                # Check that output file was created
                self.assertTrue(output_path.exists())
        finally:
            Path(json_path).unlink()


if __name__ == '__main__':
    unittest.main()
