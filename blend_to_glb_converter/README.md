# Blend2GLB - Blender到GLB转换器

一个**高质量**的Blender文件(.blend)到GLB格式转换器，使用Blender作为后端引擎确保100%准确的转换结果。

## ✨ 主要特性

- 🎯 **100%准确转换** - 使用Blender内置的GLB导出器，完全准确
- 🚀 **简单易用** - 命令行界面简洁直观
- 📦 **批量转换** - 支持批量转换整个目录
- 🎨 **完整支持** - 支持材质、纹理、动画、相机、灯光等所有Blender特性
- 🔧 **灵活配置** - 丰富的导出选项，满足各种需求
- 📊 **详细信息** - 可以查看.blend文件的详细信息
- 🌍 **跨平台** - 支持Windows、macOS、Linux

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Blender 3.0+ (将自动检测安装)

### 安装Blender

如果您还没有安装Blender，请访问 [Blender官网](https://www.blender.org/download/) 下载并安装。

**macOS:**
```bash
# 使用Homebrew安装
brew install --cask blender
```

**Windows:**
```bash
# 使用Chocolatey安装
choco install blender

# 或从官网下载安装包
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install blender

# 或使用Snap
sudo snap install blender --classic
```

### 安装转换器

```bash
git clone <repository-url>
cd blend_to_glb_converter
pip install -r requirements.txt
```

## 🛠️ 使用方法

### 基本转换

```bash
# 基本转换
python blend2glb.py input.blend -o output.glb

# 详细输出模式
python blend2glb.py input.blend -o output.glb -v
```

### 高级选项

```bash
# 包含动画和材质
python blend2glb.py model.blend -o model.glb --animations --materials

# 批量转换
python blend2glb.py -b input_dir/ -o output_dir/

# 查看文件信息
python blend2glb.py --info model.blend
```

### 命令行界面

```bash
# 使用CLI工具
python cli/main.py input.blend output.glb --verbose
```

### 编程接口

```python
from core.converter_v2 import BlendToGLBConverter

# 创建转换器实例
converter = BlendToGLBConverter()

# 检查是否可用
if converter.is_available():
    # 执行转换
    success = converter.convert(
        input_path="model.blend",
        output_path="model.glb",
        export_materials=True,
        export_animations=True,
        verbose=True
    )
    
    if success:
        print("转换成功！")
    else:
        print("转换失败")
else:
    print("Blender未找到，请先安装Blender")
```

## 📖 详细文档

- [API文档](docs/API.md)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)

## 🔧 开发

### 运行测试

```bash
python -m pytest tests/ -v
```

### 安装开发依赖

```bash
pip install -r requirements.txt
```

## 📄 许可证

本项目采用 Apache 2.0 许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

## 📞 支持

如果您遇到问题或有建议，请：

1. 查看 [Issues](https://github.com/your-repo/blend_to_glb_converter/issues)
2. 创建新的 Issue
3. 联系维护者

---

**注意**: 此转换器使用Blender作为后端引擎，确保转换结果的准确性和完整性。与其他纯Python实现不同，我们不会生成假数据或简化模型。

# With options
blend2glb input.blend output.glb --export-materials --scale 2.0 --verbose

# Show help
blend2glb --help
```

#### CLI Options

- `--verbose, -v`: Enable verbose output
- `--export-materials`: Export materials (default: enabled)
- `--export-animations`: Export animations (default: disabled)
- `--export-cameras`: Export cameras (default: disabled)
- `--export-lights`: Export lights (default: disabled)
- `--scale FACTOR`: Scale factor for the model (default: 1.0)
- `--version`: Show version information

### Python Library API

#### Basic Usage

```python
from blend_to_glb_converter import BlendToGLBConverter

# Create converter instance
converter = BlendToGLBConverter()

# Convert file
success = converter.convert("input.blend", "output.glb")

if success:
    print("Conversion successful!")
else:
    print("Conversion failed!")
```

#### Advanced Usage

```python
from blend_to_glb_converter import BlendToGLBConverter

converter = BlendToGLBConverter()

# Convert with custom options
success = converter.convert(
    input_path="complex_model.blend",
    output_path="complex_model.glb",
    export_materials=True,
    export_animations=False,
    scale=2.0
)

# Step-by-step conversion for more control
try:
    # Load .blend file data
    blend_data = converter.load_blend_data("model.blend")
    print(f"Loaded {len(blend_data.get('objects', []))} objects")
    
    # Convert to GLTF format
    gltf_data = converter.convert_to_gltf(blend_data, export_materials=True)
    
    # Export to GLB file
    success = converter.export_glb(gltf_data, "output.glb")
    
except Exception as e:
    print(f"Conversion error: {e}")
```

#### Batch Conversion

```python
import os
from blend_to_glb_converter import BlendToGLBConverter

def convert_directory(input_dir, output_dir):
    converter = BlendToGLBConverter()
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.blend'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.blend', '.glb'))
            
            success = converter.convert(input_path, output_path)
            print(f"{'✓' if success else '✗'} {filename}")

# Convert all .blend files in a directory
convert_directory("input_models/", "output_models/")
```

## 🏗️ Architecture

The project follows a modular architecture:

```
blend_to_glb_converter/
├── core/                   # Core conversion logic
│   ├── converter.py        # Main BlendToGLBConverter class
│   ├── blend_reader.py     # .blend file parser
│   └── gltf_io/           # GLTF export functionality
├── adapters/              # Data adapter layer
│   ├── base_adapter.py    # Abstract base adapter
│   └── blender_adapter.py # Blender-specific adapter
├── cli/                   # Command-line interface
│   └── main.py           # CLI entry point
├── tests/                 # Comprehensive test suite
├── examples/              # Usage examples
└── docs/                  # Documentation
```

### Key Components

- **BlendToGLBConverter**: Main orchestrator class
- **SimpleBlendReader**: Pure Python .blend file parser
- **BlenderDataAdapter**: Converts Blender data to GLTF format
- **GLTFEncoder**: Exports GLTF data to GLB files

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=core --cov=adapters --cov=cli

# Run specific test
python -m pytest tests/test_converter.py::TestBlendToGLBConverter::test_convert_materials -v
```

The test suite includes:
- Unit tests for all major components
- Integration tests for the conversion pipeline
- Error handling and edge case testing
- Mock data testing for isolated component testing

## 📚 Documentation

- **[API Documentation](docs/API.md)**: Detailed API reference
- **[Contributing Guide](CONTRIBUTING.md)**: How to contribute to the project
- **[Changelog](CHANGELOG.md)**: Version history and changes
- **[Examples](examples/)**: Usage examples and tutorials

## 🔧 Requirements

### Runtime Dependencies

- **Python 3.8+**: Core runtime
- **numpy >= 1.20.0**: Numerical computations
- **Pillow >= 8.0.0**: Image processing (optional)

### Development Dependencies

- **pytest >= 6.0.0**: Testing framework
- **pytest-cov >= 2.10.0**: Coverage reporting

See [requirements.txt](requirements.txt) for complete dependency list.

## ⚠️ Current Limitations

- **Basic Mesh Support**: Full geometry processing not yet implemented
- **Limited Materials**: Basic PBR properties only
- **No Animations**: Animation export not supported in v0.1.0
- **No Textures**: Image/texture export not implemented
- **Simplified Parsing**: Not all .blend block types supported

## 🗺️ Roadmap

### Version 0.2.0
- [ ] Enhanced mesh geometry processing
- [ ] Full material and texture support
- [ ] Improved .blend file parsing

### Version 0.3.0
- [ ] Animation export capabilities
- [ ] Camera and light export
- [ ] Performance optimizations

### Future Versions
- [ ] Additional file format support (FBX, OBJ)
- [ ] GUI application
- [ ] Blender addon integration

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Coding standards and guidelines
- Testing requirements
- Pull request process

### Quick Start for Contributors

```bash
# Fork and clone the repository
git clone <your-fork-url>
cd blend_to_glb_converter

# Set up development environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Run tests to verify setup
python -m pytest tests/ -v

# Create a feature branch
git checkout -b feature/your-feature-name
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Blender Foundation for the GLTF export functionality
- The GLTF specification contributors
- Python community for excellent libraries and tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Project Wiki](https://github.com/your-repo/wiki)

## 📊 Project Status

- **Version**: 0.1.0
- **Status**: Active Development
- **Python Support**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Platforms**: Windows, macOS, Linux