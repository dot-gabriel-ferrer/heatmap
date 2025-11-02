"""
Image Utilities Module

This module provides utility functions for image processing tasks.
"""

import logging
from typing import Tuple
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def crop_image(
    input_path: str,
    output_path: str,
    crop_box: Tuple[int, int, int, int]
) -> None:
    """
    Crop an image to a specified bounding box.
    
    Args:
        input_path: Path to the input image
        output_path: Path to save the cropped image
        crop_box: Tuple of (left, top, right, bottom) coordinates
    
    Raises:
        FileNotFoundError: If the input image does not exist
        IOError: If there's an error reading or writing the image
    """
    try:
        with Image.open(input_path) as img:
            cropped = img.crop(crop_box)
            cropped.save(output_path)
        
        logger.info(f"Cropped {input_path} to {output_path}")
    
    except FileNotFoundError as e:
        logger.error(f"Image file not found: {e}")
        raise
    except IOError as e:
        logger.error(f"Error processing image: {e}")
        raise


def resize_image(
    input_path: str,
    output_path: str,
    size: Tuple[int, int],
    maintain_aspect: bool = True
) -> None:
    """
    Resize an image to specified dimensions.
    
    Args:
        input_path: Path to the input image
        output_path: Path to save the resized image
        size: Tuple of (width, height) for the new size
        maintain_aspect: If True, maintains aspect ratio using thumbnail method
    
    Raises:
        FileNotFoundError: If the input image does not exist
        IOError: If there's an error reading or writing the image
    """
    try:
        with Image.open(input_path) as img:
            if maintain_aspect:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                img.save(output_path)
            else:
                resized = img.resize(size, Image.Resampling.LANCZOS)
                resized.save(output_path)
        
        logger.info(f"Resized {input_path} to {output_path}")
    
    except FileNotFoundError as e:
        logger.error(f"Image file not found: {e}")
        raise
    except IOError as e:
        logger.error(f"Error processing image: {e}")
        raise
