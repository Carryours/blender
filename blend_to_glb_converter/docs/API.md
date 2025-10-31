# API Documentation

This document provides detailed information about the Blend to GLB Converter API.

## Table of Contents

- [Core Classes](#core-classes)
- [Adapters](#adapters)
- [Utilities](#utilities)
- [Examples](#examples)

## Core Classes

### BlendToGLBConverter

The main converter class that orchestrates the conversion process.

```python
from blend_to_glb_converter import BlendToGLBConverter

converter = BlendToGLBConverter()
```

#### Methods

##### `__init__(self, adapter=None)`

Initialize the converter with an optional data adapter.

**Parameters:**
- `adapter` (BaseDataAdapter, optional): Custom data adapter. Defaults to BlenderDataAdapter.

**Example:**
```python
from blend_to_glb_converter import BlendToGLBConverter
from blend_to_glb_converter.adapters import BlenderDataAdapter

# Use default adapter
converter = BlendToGLBConverter()

# Use custom adapter
custom_adapter = BlenderDataAdapter()
converter = BlendToGLBConverter(adapter=custom_adapter)
```

##### `convert(self, input_path: str, output_path: str, **options) -> bool`

Convert a .blend file to GLB format.

**Parameters:**
- `input_path` (str): Path to the input .blend file
- `output_path` (str): Path for the output .glb file
- `**options`: Additional conversion options

**Options:**
- `export_materials` (bool): Export materials (default: True)
- `export_animations` (bool): Export animations (default: False)
- `export_cameras` (bool): Export cameras (default: False)
- `export_lights` (bool): Export lights (default: False)
- `scale` (float): Scale factor for the model (default: 1.0)

**Returns:**
- `bool`: True if conversion successful, False otherwise

**Example:**
```python
success = converter.convert(
    input_path="model.blend",
    output_path="model.glb",
    export_materials=True,
    scale=2.0
)

if success:
    print("Conversion successful!")
else:
    print("Conversion failed!")
```

##### `load_blend_data(self, filepath: str) -> Dict[str, Any]`

Load and parse .blend file data.

**Parameters:**
- `filepath` (str): Path to the .blend file

**Returns:**
- `Dict[str, Any]`: Parsed blend file data

**Example:**
```python
blend_data = converter.load_blend_data("model.blend")
print(f"Found {len(blend_data.get('objects', []))} objects")
```

##### `convert_to_gltf(self, blend_data: Dict[str, Any], **options) -> Dict[str, Any]`

Convert blend data to GLTF format.

**Parameters:**
- `blend_data` (Dict[str, Any]): Parsed blend file data
- `**options`: Conversion options

**Returns:**
- `Dict[str, Any]`: GLTF format data

**Example:**
```python
blend_data = converter.load_blend_data("model.blend")
gltf_data = converter.convert_to_gltf(blend_data, export_materials=True)
```

##### `export_glb(self, gltf_data: Dict[str, Any], output_path: str) -> bool`

Export GLTF data to GLB file.

**Parameters:**
- `gltf_data` (Dict[str, Any]): GLTF format data
- `output_path` (str): Output file path

**Returns:**
- `bool`: True if export successful, False otherwise

**Example:**
```python
success = converter.export_glb(gltf_data, "output.glb")
```

## Adapters

### BaseDataAdapter

Abstract base class for data adapters.

```python
from blend_to_glb_converter.adapters import BaseDataAdapter

class CustomAdapter(BaseDataAdapter):
    def load_data(self, filepath: str) -> Dict[str, Any]:
        # Custom implementation
        pass
    
    def convert_to_gltf(self, data: Dict[str, Any], **options) -> Dict[str, Any]:
        # Custom implementation
        pass
```

#### Abstract Methods

##### `load_data(self, filepath: str) -> Dict[str, Any]`

Load data from the specified file.

**Parameters:**
- `filepath` (str): Path to the input file

**Returns:**
- `Dict[str, Any]`: Loaded data

##### `convert_to_gltf(self, data: Dict[str, Any], **options) -> Dict[str, Any]`

Convert loaded data to GLTF format.

**Parameters:**
- `data` (Dict[str, Any]): Loaded data
- `**options`: Conversion options

**Returns:**
- `Dict[str, Any]`: GLTF format data

### BlenderDataAdapter

Concrete adapter for Blender .blend files.

```python
from blend_to_glb_converter.adapters import BlenderDataAdapter

adapter = BlenderDataAdapter()
```

#### Methods

##### `load_data(self, filepath: str) -> Dict[str, Any]`

Load data from a .blend file.

**Parameters:**
- `filepath` (str): Path to the .blend file

**Returns:**
- `Dict[str, Any]`: Blend file data including objects, materials, meshes

**Example:**
```python
adapter = BlenderDataAdapter()
data = adapter.load_data("model.blend")

print(f"Objects: {len(data.get('objects', []))}")
print(f"Materials: {len(data.get('materials', []))}")
print(f"Meshes: {len(data.get('meshes', []))}")
```

##### `convert_to_gltf(self, data: Dict[str, Any], **options) -> Dict[str, Any]`

Convert blend data to GLTF format.

**Parameters:**
- `data` (Dict[str, Any]): Blend file data
- `**options`: Conversion options

**Returns:**
- `Dict[str, Any]`: GLTF format data

**Example:**
```python
gltf_data = adapter.convert_to_gltf(
    data,
    export_materials=True,
    scale=1.0
)
```

## Utilities

### SimpleBlendReader

Low-level .blend file parser.

```python
from blend_to_glb_converter.core.blend_reader import SimpleBlendReader

reader = SimpleBlendReader("model.blend")
```

#### Methods

##### `__init__(self, filepath: str)`

Initialize the reader with a .blend file path.

**Parameters:**
- `filepath` (str): Path to the .blend file

##### `read(self) -> Dict[str, Any]`

Read and parse the .blend file.

**Returns:**
- `Dict[str, Any]`: Parsed file data

**Example:**
```python
reader = SimpleBlendReader("model.blend")
data = reader.read()

for block in data.get('blocks', []):
    print(f"Block: {block.code}, Count: {block.count}")
```

### GLTFEncoder

GLTF/GLB file encoder.

```python
from blend_to_glb_converter.core.gltf_io import GLTFEncoder

encoder = GLTFEncoder()
```

#### Methods

##### `encode_to_glb(self, gltf_data: Dict[str, Any], output_path: str) -> bool`

Encode GLTF data to GLB file.

**Parameters:**
- `gltf_data` (Dict[str, Any]): GLTF format data
- `output_path` (str): Output file path

**Returns:**
- `bool`: True if encoding successful, False otherwise

## Examples

### Basic Conversion

```python
from blend_to_glb_converter import BlendToGLBConverter

# Create converter
converter = BlendToGLBConverter()

# Convert file
success = converter.convert("input.blend", "output.glb")

if success:
    print("Conversion completed successfully!")
else:
    print("Conversion failed!")
```

### Advanced Conversion with Options

```python
from blend_to_glb_converter import BlendToGLBConverter

converter = BlendToGLBConverter()

# Convert with custom options
success = converter.convert(
    input_path="complex_model.blend",
    output_path="complex_model.glb",
    export_materials=True,
    export_animations=False,
    export_cameras=True,
    export_lights=True,
    scale=2.0
)

print(f"Conversion {'successful' if success else 'failed'}")
```

### Step-by-Step Conversion

```python
from blend_to_glb_converter import BlendToGLBConverter

converter = BlendToGLBConverter()

try:
    # Step 1: Load blend data
    print("Loading .blend file...")
    blend_data = converter.load_blend_data("model.blend")
    print(f"Loaded {len(blend_data.get('objects', []))} objects")
    
    # Step 2: Convert to GLTF
    print("Converting to GLTF...")
    gltf_data = converter.convert_to_gltf(
        blend_data,
        export_materials=True,
        scale=1.0
    )
    print("GLTF conversion complete")
    
    # Step 3: Export GLB
    print("Exporting GLB...")
    success = converter.export_glb(gltf_data, "output.glb")
    
    if success:
        print("Export successful!")
    else:
        print("Export failed!")
        
except Exception as e:
    print(f"Error during conversion: {e}")
```

### Custom Adapter

```python
from blend_to_glb_converter import BlendToGLBConverter
from blend_to_glb_converter.adapters import BaseDataAdapter
from typing import Dict, Any

class CustomDataAdapter(BaseDataAdapter):
    def load_data(self, filepath: str) -> Dict[str, Any]:
        # Custom data loading logic
        return {
            'objects': [],
            'materials': [],
            'meshes': []
        }
    
    def convert_to_gltf(self, data: Dict[str, Any], **options) -> Dict[str, Any]:
        # Custom GLTF conversion logic
        return {
            'asset': {'version': '2.0'},
            'scenes': [],
            'nodes': [],
            'meshes': [],
            'materials': []
        }

# Use custom adapter
custom_adapter = CustomDataAdapter()
converter = BlendToGLBConverter(adapter=custom_adapter)

success = converter.convert("input.blend", "output.glb")
```

### Batch Conversion

```python
import os
from blend_to_glb_converter import BlendToGLBConverter

def batch_convert(input_dir: str, output_dir: str):
    """Convert all .blend files in a directory"""
    converter = BlendToGLBConverter()
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all .blend files
    blend_files = [f for f in os.listdir(input_dir) if f.endswith('.blend')]
    
    results = []
    for blend_file in blend_files:
        input_path = os.path.join(input_dir, blend_file)
        output_file = blend_file.replace('.blend', '.glb')
        output_path = os.path.join(output_dir, output_file)
        
        print(f"Converting {blend_file}...")
        success = converter.convert(input_path, output_path)
        
        results.append({
            'file': blend_file,
            'success': success
        })
        
        if success:
            print(f"✓ {blend_file} -> {output_file}")
        else:
            print(f"✗ Failed to convert {blend_file}")
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    print(f"\nConversion complete: {successful}/{total} files successful")
    
    return results

# Usage
results = batch_convert("input_models/", "output_models/")
```

## Error Handling

The API uses standard Python exceptions. Common exceptions include:

- `FileNotFoundError`: Input file not found
- `ValueError`: Invalid parameters or data
- `IOError`: File read/write errors
- `RuntimeError`: Conversion errors

**Example:**
```python
from blend_to_glb_converter import BlendToGLBConverter

converter = BlendToGLBConverter()

try:
    success = converter.convert("model.blend", "output.glb")
except FileNotFoundError:
    print("Input file not found")
except ValueError as e:
    print(f"Invalid parameter: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Tips

1. **Reuse converter instances** for multiple conversions
2. **Use appropriate scale factors** to avoid precision issues
3. **Disable unused exports** (animations, cameras, lights) for better performance
4. **Process large files in chunks** when possible
5. **Use virtual environments** to avoid dependency conflicts

## Limitations

- Basic mesh conversion (full geometry processing not implemented)
- Limited material property support
- No animation support in current version
- No texture/image export
- Simplified .blend file parsing