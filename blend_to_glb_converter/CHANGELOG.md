# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-28

### Added
- Initial release of Blend to GLB Converter
- Core conversion functionality from .blend to .glb format
- Modular architecture with adapters, core, and CLI components
- Command-line interface (`blend2glb`) for easy conversion
- Python library API for programmatic use
- Support for basic mesh, material, and object conversion
- Coordinate system conversion (Blender Z-up to GLTF Y-up)
- Comprehensive test suite with 10 test cases
- Documentation and usage examples
- Virtual environment support
- Cross-platform compatibility (macOS, Linux, Windows)

### Features
- **Core Converter**: Main conversion engine with `BlendToGLBConverter` class
- **Blend Reader**: Python-only .blend file parser (no Blender dependency)
- **Data Adapters**: Extensible adapter system for different data sources
- **GLTF IO**: Extracted and adapted GLTF export functionality from Blender
- **CLI Tool**: User-friendly command-line interface with multiple options
- **Testing**: Comprehensive unit tests for all major components
- **Examples**: Basic usage examples and advanced scenarios

### Technical Details
- Pure Python implementation (no Blender runtime dependency)
- Supports gzipped .blend files
- Handles materials with PBR properties
- Converts coordinate systems automatically
- Extensible architecture for future enhancements

### Dependencies
- numpy >= 1.20.0
- pytest >= 6.0.0 (development)
- pytest-cov >= 2.10.0 (development)
- Pillow >= 8.0.0 (optional, for image processing)

### Known Limitations
- Basic mesh conversion (full geometry processing not yet implemented)
- Limited material property support
- No animation support in this version
- No texture/image export
- Simplified .blend file parsing (not all block types supported)

### Future Roadmap
- Enhanced mesh geometry processing
- Full material and texture support
- Animation export capabilities
- Camera and light export
- Performance optimizations
- Additional file format support