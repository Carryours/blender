#!/usr/bin/env python3
"""
Basic Usage Example for Blend to GLB Converter

This example demonstrates how to use the converter library programmatically.
"""

import sys
import os
from pathlib import Path

# Add the converter to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.converter_v2 import BlendToGLBConverter


def main():
    """Basic usage example"""
    
    # Create converter instance
    converter = BlendToGLBConverter()
    
    # Example file paths (adjust these to your actual files)
    input_file = "example_model.blend"
    output_file = "example_model.glb"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found.")
        print("Please create a .blend file or update the path in this example.")
        return
    
    # Conversion options
    options = {
        'verbose': True,
        'export_materials': True,
        'export_animations': False,
        'scale': 1.0
    }
    
    print("Starting conversion...")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Options: {options}")
    print()
    
    # Perform conversion
    success = converter.convert(input_file, output_file, **options)
    
    if success:
        print("✅ Conversion completed successfully!")
        print(f"GLB file saved to: {output_file}")
    else:
        print("❌ Conversion failed!")
        print("Check the console output for error details.")


def advanced_usage_example():
    """Advanced usage with custom settings"""
    
    converter = BlendToGLBConverter()
    
    # Multiple conversions with different settings
    conversions = [
        {
            'input': 'model1.blend',
            'output': 'model1_basic.glb',
            'options': {'export_materials': True, 'export_animations': False}
        },
        {
            'input': 'model2.blend', 
            'output': 'model2_with_animations.glb',
            'options': {'export_materials': True, 'export_animations': True}
        },
        {
            'input': 'scene.blend',
            'output': 'scene_scaled.glb',
            'options': {'scale': 0.5, 'export_cameras': True, 'export_lights': True}
        }
    ]
    
    for conversion in conversions:
        if os.path.exists(conversion['input']):
            print(f"Converting {conversion['input']}...")
            success = converter.convert(
                conversion['input'],
                conversion['output'],
                **conversion['options']
            )
            
            if success:
                print(f"✅ {conversion['output']} created successfully")
            else:
                print(f"❌ Failed to create {conversion['output']}")
        else:
            print(f"⚠️  Skipping {conversion['input']} (file not found)")


if __name__ == '__main__':
    print("=== Blend to GLB Converter - Basic Usage Example ===")
    print()
    
    # Run basic example
    main()
    
    print()
    print("=== Advanced Usage Example ===")
    print()
    
    # Run advanced example
    advanced_usage_example()