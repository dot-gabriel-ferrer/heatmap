#!/usr/bin/env python3
"""
Heatmap Generator CLI

Command-line interface for generating heatmaps from point cloud data or
JSON coordinate files.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

import numpy as np

from heatmap.heatmap_generator import create_heatmap, create_heatmap_from_points
from animation.togif import create_gif
from animation.images import overlay_images
from motion.motion import update_coordinates


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description='Generate heatmaps from geographic point cloud data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate heatmap from JSON file
  %(prog)s generate --input data.json --output heatmap.png
  
  # Generate heatmap with custom parameters
  %(prog)s generate --input data.json --output heatmap.png --grid-size 2 --bandwidth 15
  
  # Create animated heatmap
  %(prog)s animate --frames 100 --output animation.gif
  
  # Overlay heatmap on background
  %(prog)s overlay --background map.png --heatmap heat.png --output result.png
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a heatmap from data')
    generate_parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input JSON file with coordinate data'
    )
    generate_parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output path for heatmap image'
    )
    generate_parser.add_argument(
        '--grid-size',
        type=float,
        default=1.0,
        help='Size of grid cells (default: 1.0)'
    )
    generate_parser.add_argument(
        '--bandwidth',
        type=float,
        default=10.0,
        help='Bandwidth parameter for KDE (default: 10.0)'
    )
    generate_parser.add_argument(
        '--colormap',
        default='jet',
        help='Matplotlib colormap name (default: jet)'
    )
    generate_parser.add_argument(
        '--interpolation',
        default='gaussian',
        help='Interpolation method (default: gaussian)'
    )
    
    # Animate command
    animate_parser = subparsers.add_parser('animate', help='Create animated heatmap')
    animate_parser.add_argument(
        '--frames',
        type=int,
        default=100,
        help='Number of frames to generate (default: 100)'
    )
    animate_parser.add_argument(
        '--points',
        type=int,
        default=100,
        help='Number of points in simulation (default: 100)'
    )
    animate_parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output path for GIF animation'
    )
    animate_parser.add_argument(
        '--background',
        help='Optional background image to overlay heatmap on'
    )
    animate_parser.add_argument(
        '--duration',
        type=int,
        default=20,
        help='Frame duration in milliseconds (default: 20)'
    )
    animate_parser.add_argument(
        '--grid-size',
        type=float,
        default=10.0,
        help='Size of grid cells (default: 10.0)'
    )
    animate_parser.add_argument(
        '--bandwidth',
        type=float,
        default=10.0,
        help='Bandwidth parameter for KDE (default: 10.0)'
    )
    
    # Overlay command
    overlay_parser = subparsers.add_parser('overlay', help='Overlay heatmap on background')
    overlay_parser.add_argument(
        '--background',
        required=True,
        help='Background image path'
    )
    overlay_parser.add_argument(
        '--heatmap',
        required=True,
        help='Heatmap image path'
    )
    overlay_parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output path for composite image'
    )
    overlay_parser.add_argument(
        '--crop',
        help='Crop box as "left,top,right,bottom"'
    )
    
    # GIF command
    gif_parser = subparsers.add_parser('gif', help='Create GIF from image sequence')
    gif_parser.add_argument(
        '--input',
        required=True,
        help='Input pattern (e.g., "frames/frame*.png")'
    )
    gif_parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output path for GIF'
    )
    gif_parser.add_argument(
        '--duration',
        type=int,
        default=20,
        help='Frame duration in milliseconds (default: 20)'
    )
    gif_parser.add_argument(
        '--loop',
        type=int,
        default=0,
        help='Number of loops, 0 for infinite (default: 0)'
    )
    gif_parser.add_argument(
        '--quality',
        type=int,
        default=50,
        help='GIF quality, 1-100 (default: 50)'
    )
    gif_parser.add_argument(
        '--optimize',
        action='store_true',
        help='Optimize GIF palette'
    )
    
    return parser


def cmd_generate(args: argparse.Namespace) -> int:
    """Execute generate command."""
    try:
        create_heatmap(
            output_path=args.output,
            json_file=args.input,
            grid_size=args.grid_size,
            bandwidth=args.bandwidth,
            colormap=args.colormap,
            interpolation=args.interpolation
        )
        logger.info(f"Heatmap generated successfully: {args.output}")
        return 0
    except Exception as e:
        logger.error(f"Failed to generate heatmap: {e}")
        return 1


def cmd_animate(args: argparse.Namespace) -> int:
    """Execute animate command."""
    try:
        # Create output directory for frames
        temp_dir = Path("temp_frames")
        temp_dir.mkdir(exist_ok=True)
        
        # Initialize random point cloud
        x = np.random.randint(0, 100, args.points)
        y = np.random.randint(0, 100, args.points)
        
        logger.info(f"Generating {args.frames} frames...")
        
        for i in range(args.frames):
            frame_path = temp_dir / f"frame_{i:04d}.png"
            
            # Generate heatmap
            create_heatmap_from_points(
                str(frame_path),
                x, y,
                grid_size=args.grid_size,
                bandwidth=args.bandwidth
            )
            
            # Overlay on background if provided
            if args.background:
                overlay_images(args.background, str(frame_path), str(frame_path))
            
            # Update positions for next frame
            import random
            x_sign = random.choice([1, -1])
            y_sign = random.choice([1, -1])
            x_delta = np.random.random(args.points) * x_sign
            y_delta = np.random.random(args.points) * y_sign
            x, y = update_coordinates(x, y, x_delta, y_delta)
            
            if (i + 1) % 10 == 0:
                logger.info(f"Generated {i + 1}/{args.frames} frames")
        
        # Create GIF
        logger.info("Creating GIF animation...")
        create_gif(
            str(temp_dir / "frame_*.png"),
            args.output,
            duration=args.duration
        )
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        logger.info(f"Animation created successfully: {args.output}")
        return 0
    
    except Exception as e:
        logger.error(f"Failed to create animation: {e}")
        return 1


def cmd_overlay(args: argparse.Namespace) -> int:
    """Execute overlay command."""
    try:
        crop_box = None
        if args.crop:
            crop_box = tuple(map(int, args.crop.split(',')))
        
        overlay_images(
            args.background,
            args.heatmap,
            args.output,
            crop_box
        )
        logger.info(f"Image overlay created successfully: {args.output}")
        return 0
    
    except Exception as e:
        logger.error(f"Failed to overlay images: {e}")
        return 1


def cmd_gif(args: argparse.Namespace) -> int:
    """Execute gif command."""
    try:
        create_gif(
            args.input,
            args.output,
            duration=args.duration,
            loop=args.loop,
            quality=args.quality,
            optimize=args.optimize
        )
        logger.info(f"GIF created successfully: {args.output}")
        return 0
    
    except Exception as e:
        logger.error(f"Failed to create GIF: {e}")
        return 1


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute appropriate command
    commands = {
        'generate': cmd_generate,
        'animate': cmd_animate,
        'overlay': cmd_overlay,
        'gif': cmd_gif
    }
    
    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())
