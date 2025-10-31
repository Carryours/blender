# Contributing to Blend to GLB Converter

Thank you for your interest in contributing to the Blend to GLB Converter project! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd blend_to_glb_converter
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Run tests to verify setup**
   ```bash
   python -m pytest tests/ -v
   ```

## Project Structure

```
blend_to_glb_converter/
├── core/                   # Core conversion logic
│   ├── converter.py        # Main converter class
│   ├── blend_reader.py     # .blend file parser
│   └── gltf_io/           # GLTF export functionality
├── adapters/              # Data adapter layer
│   ├── base_adapter.py    # Abstract base adapter
│   └── blender_adapter.py # Blender data adapter
├── cli/                   # Command-line interface
│   └── main.py           # CLI entry point
├── tests/                 # Test suite
├── examples/              # Usage examples
└── docs/                  # Documentation
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Use meaningful variable and function names

### Code Formatting

```python
def convert_coordinates(position: List[float]) -> List[float]:
    """
    Convert coordinates from Blender to GLTF coordinate system.
    
    Args:
        position: [x, y, z] in Blender coordinate system
        
    Returns:
        [x, y, z] in GLTF coordinate system
    """
    x, y, z = position
    return [x, z, -y]
```

### Import Organization

```python
# Standard library imports
import os
import sys
from typing import Dict, List, Any

# Third-party imports
import numpy as np

# Local imports
from core.converter import BlendToGLBConverter
from adapters.base_adapter import BaseDataAdapter
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=core --cov=adapters --cov=cli

# Run specific test file
python -m pytest tests/test_converter.py -v
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies when appropriate

```python
def test_material_conversion(self):
    """Test material conversion to GLTF format"""
    material = {
        'name': 'TestMaterial',
        'base_color': [1.0, 0.0, 0.0, 1.0],
        'metallic': 0.5,
        'roughness': 0.3
    }
    
    gltf_material = self.converter._convert_material_to_gltf(material)
    
    self.assertEqual(gltf_material['name'], 'TestMaterial')
    self.assertEqual(gltf_material['pbrMetallicRoughness']['baseColorFactor'], 
                     [1.0, 0.0, 0.0, 1.0])
```

## Submitting Changes

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   python -m pytest tests/ -v
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

5. **Push to your fork and create a pull request**

### Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Examples:
```
Add support for texture export

- Implement texture extraction from .blend files
- Add texture conversion to GLTF format
- Update tests for texture functionality

Fixes #123
```

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to reproduce**: Detailed steps to reproduce the problem
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, Python version, package versions
- **Sample files**: If applicable, provide sample .blend files

### Feature Requests

For feature requests, please include:

- **Description**: Clear description of the proposed feature
- **Use case**: Why this feature would be useful
- **Implementation ideas**: Any thoughts on how it could be implemented

## Development Guidelines

### Adding New Features

1. **Design first**: Consider the architecture and how the feature fits
2. **Start with tests**: Write tests that define the expected behavior
3. **Implement incrementally**: Break large features into smaller parts
4. **Document as you go**: Update documentation and examples

### Performance Considerations

- Profile code for performance bottlenecks
- Use appropriate data structures
- Consider memory usage for large .blend files
- Optimize hot paths in the conversion process

### Compatibility

- Maintain compatibility with Python 3.8+
- Test on multiple platforms when possible
- Consider backward compatibility for API changes

## Getting Help

- **Documentation**: Check the README and examples first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions and ideas

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for their contributions
- README.md contributors section
- Release notes for significant contributions

Thank you for contributing to the Blend to GLB Converter project!