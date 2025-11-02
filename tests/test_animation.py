"""
Unit tests for animation.images module.
"""

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from animation.images import overlay_images


class TestOverlayImages(unittest.TestCase):
    """Test image overlay functionality."""
    
    def setUp(self):
        """Create temporary test images."""
        self.tmpdir = tempfile.mkdtemp()
        
        # Create a simple background image (100x100, blue)
        background = Image.new('RGB', (100, 100), color='blue')
        self.background_path = Path(self.tmpdir) / 'background.png'
        background.save(self.background_path)
        
        # Create a simple overlay image with transparency (50x50, red with alpha)
        overlay = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        self.overlay_path = Path(self.tmpdir) / 'overlay.png'
        overlay.save(self.overlay_path)
        
        self.output_path = Path(self.tmpdir) / 'output.png'
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.tmpdir)
    
    def test_overlay_images_basic(self):
        """Test basic image overlay."""
        overlay_images(
            str(self.background_path),
            str(self.overlay_path),
            str(self.output_path),
            crop_box=(10, 10, 60, 60)
        )
        
        # Check that output file was created
        self.assertTrue(self.output_path.exists())
        
        # Check that output image has expected dimensions
        with Image.open(self.output_path) as img:
            self.assertEqual(img.size, (50, 50))
    
    def test_overlay_images_default_crop(self):
        """Test overlay with default crop box."""
        # Create larger images for default crop
        background = Image.new('RGB', (600, 600), color='blue')
        overlay = Image.new('RGBA', (600, 600), color=(255, 0, 0, 128))
        
        bg_path = Path(self.tmpdir) / 'bg_large.png'
        ov_path = Path(self.tmpdir) / 'ov_large.png'
        out_path = Path(self.tmpdir) / 'out_large.png'
        
        background.save(bg_path)
        overlay.save(ov_path)
        
        overlay_images(str(bg_path), str(ov_path), str(out_path))
        
        self.assertTrue(out_path.exists())
    
    def test_overlay_images_missing_file(self):
        """Test error handling for missing file."""
        with self.assertRaises(FileNotFoundError):
            overlay_images(
                'nonexistent.png',
                str(self.overlay_path),
                str(self.output_path)
            )


if __name__ == '__main__':
    unittest.main()
