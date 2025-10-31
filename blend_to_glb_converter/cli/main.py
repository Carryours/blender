#!/usr/bin/env python3
"""
Command Line Interface for Blend to GLB Converter

Usage:
    blend2glb input.blend output.glb [options]
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.converter_v2 import BlendToGLBConverter


def parse_arguments():
    """Parse command line arguments"""
    
    parser = argparse.ArgumentParser(
        description='Convert Blender .blend files to GLB format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    blend2glb model.blend model.glb
    blend2glb input.blend output.glb --verbose
    blend2glb scene.blend scene.glb --export-materials --export-animations
        """
    )
    
    parser.add_argument(
        'input',
        help='Input .blend file path'
    )
    
    parser.add_argument(
        'output',
        help='Output .glb file path'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--export-materials',
        action='store_true',
        default=True,
        help='Export materials (default: True)'
    )
    
    parser.add_argument(
        '--export-animations',
        action='store_true',
        default=False,
        help='Export animations (default: False)'
    )
    
    parser.add_argument(
        '--export-cameras',
        action='store_true',
        default=False,
        help='Export cameras (default: False)'
    )
    
    parser.add_argument(
        '--export-lights',
        action='store_true',
        default=False,
        help='Export lights (default: False)'
    )
    
    parser.add_argument(
        '--scale',
        type=float,
        default=1.0,
        help='Scale factor for the exported model (default: 1.0)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Blend to GLB Converter v0.1.0'
    )
    
    return parser.parse_args()


def validate_inputs(args):
    """Validate input arguments"""
    
    # Check input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return False
    
    if not args.input.lower().endswith('.blend'):
        print(f"Error: Input file '{args.input}' is not a .blend file.")
        return False
    
    # Check output directory
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            print(f"Error: Cannot create output directory '{output_dir}': {e}")
            return False
    
    # Check output extension
    if not args.output.lower().endswith('.glb'):
        print(f"Warning: Output file '{args.output}' does not have .glb extension.")
    
    return True


def main():
    """Main entry point for the CLI"""
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate inputs
        if not validate_inputs(args):
            sys.exit(1)
        
        # Set up conversion options
        options = {
            'verbose': args.verbose,
            'export_materials': args.export_materials,
            'export_animations': args.export_animations,
            'export_cameras': args.export_cameras,
            'export_lights': args.export_lights,
            'scale': args.scale
        }
        
        if args.verbose:
            print(f"Input file: {args.input}")
            print(f"Output file: {args.output}")
            print(f"Options: {options}")
            print()
        
        # Create converter and perform conversion
        converter = BlendToGLBConverter()
        success = converter.convert(args.input, args.output, **options)
        
        if success:
            print(f"Successfully converted '{args.input}' to '{args.output}'")
            sys.exit(0)
        else:
            print(f"Failed to convert '{args.input}' to '{args.output}'")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nConversion interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()