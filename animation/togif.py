"""
GIF Animation Module

This module provides functionality for creating GIF animations from a sequence
of image files.
"""

import contextlib
import glob
import logging
from pathlib import Path
from typing import Optional

from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_gif(
    input_pattern: str,
    output_path: str,
    duration: int = 20,
    loop: int = 0,
    quality: int = 50,
    optimize: bool = False
) -> None:
    """
    Create an animated GIF from a sequence of images.
    
    Args:
        input_pattern: Glob pattern for input images (e.g., "frames/frame*.png")
        output_path: Path to save the output GIF
        duration: Duration of each frame in milliseconds (default: 20)
        loop: Number of times to loop the animation, 0 for infinite (default: 0)
        quality: JPEG quality for GIF compression, 1-100 (default: 50)
        optimize: Whether to optimize the GIF palette (default: False)
    
    Raises:
        ValueError: If no images match the input pattern
        IOError: If there's an error reading images or writing the GIF
    """
    try:
        # Get sorted list of image files
        image_files = sorted(glob.glob(input_pattern))
        
        if not image_files:
            raise ValueError(f"No images found matching pattern: {input_pattern}")
        
        logger.info(f"Found {len(image_files)} images to process")
        
        # Use context manager to automatically close opened images
        with contextlib.ExitStack() as stack:
            # Lazily load images
            images = (
                stack.enter_context(Image.open(file))
                for file in image_files
            )
            
            # Extract first image from iterator
            first_image = next(images)
            
            # Save as animated GIF
            first_image.save(
                fp=output_path,
                format='GIF',
                append_images=images,
                save_all=True,
                duration=duration,
                loop=loop,
                quality=quality,
                optimize=optimize
            )
        
        logger.info(f"Created GIF animation: {output_path}")
    
    except ValueError as e:
        logger.error(str(e))
        raise
    except IOError as e:
        logger.error(f"Error creating GIF: {e}")
        raise


def create_gif_from_directory(
    input_dir: str,
    output_path: str,
    extension: str = "png",
    duration: int = 20,
    loop: int = 0,
    quality: int = 50,
    optimize: bool = False
) -> None:
    """
    Create an animated GIF from all images in a directory.
    
    Args:
        input_dir: Directory containing input images
        output_path: Path to save the output GIF
        extension: File extension to match (default: "png")
        duration: Duration of each frame in milliseconds (default: 20)
        loop: Number of times to loop the animation, 0 for infinite (default: 0)
        quality: JPEG quality for GIF compression, 1-100 (default: 50)
        optimize: Whether to optimize the GIF palette (default: False)
    """
    pattern = f"{input_dir}/*.{extension}"
    create_gif(pattern, output_path, duration, loop, quality, optimize)
