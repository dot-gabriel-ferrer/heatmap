"""
Image Manipulation Module

This module provides functionality for overlaying images, useful for
compositing heatmaps onto background maps.
"""

import logging
from typing import Optional, Tuple
from PIL import Image

logger = logging.getLogger(__name__)


def overlay_images(
    background_path: str,
    overlay_path: str,
    output_path: str,
    crop_box: Optional[Tuple[int, int, int, int]] = None
) -> None:
    """
    Overlay a transparent image onto a background image.
    
    Args:
        background_path: Path to the background image
        overlay_path: Path to the overlay image (should have transparency)
        output_path: Path to save the composite image
        crop_box: Optional tuple (left, top, right, bottom) for cropping the result.
                 If None, uses default crop (80, 22, 540, 480)
    
    Raises:
        FileNotFoundError: If input images do not exist
        IOError: If there's an error reading or writing images
    """
    try:
        with Image.open(background_path) as background:
            with Image.open(overlay_path) as overlay:
                # Create a copy to avoid modifying the original
                composite = background.copy()
                composite.paste(overlay, mask=overlay)
                
                # Apply cropping if specified
                if crop_box is None:
                    crop_box = (80, 22, 540, 480)  # Default crop box
                
                cropped = composite.crop(crop_box)
                cropped.save(output_path)
                
        logger.info(f"Overlaid {overlay_path} onto {background_path}, saved to {output_path}")
    
    except FileNotFoundError as e:
        logger.error(f"Image file not found: {e}")
        raise
    except IOError as e:
        logger.error(f"Error processing images: {e}")
        raise

