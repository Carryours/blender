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

# 或者从官网下载dmg文件安装到Applications文件夹
```

**Windows:**
```bash
# 下载并运行安装程序
# https://www.blender.org/download/
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install blender

# Fedora
sudo dnf install blender

# Arch
sudo pacman -S blender

# 或使用Snap (推荐)
sudo snap install blender --classic
```

### 安装转换器

```bash
cd blend_to_glb_converter
# 无需安装额外依赖，直接使用
```

## 📖 使用方法

### 基本用法

```bash
# 最简单的转换
python blend2glb.py input.blend -o output.glb

# 自动生成输出文件名
python blend2glb.py model.blend
# 将生成 model.glb
```

### 高级选项

```bash
# 转换并包含动画
python blend2glb.py animated_model.blend -o output.glb --animations

# 转换并包含所有内容（材质、动画、相机、灯光）
python blend2glb.py scene.blend -o scene.glb --animations --cameras --lights

# 详细输出模式（显示转换过程）
python blend2glb.py input.blend -o output.glb -v

# 不导出材质
python blend2glb.py input.blend -o output.glb --no-materials
```

### 批量转换

```bash
# 转换目录中的所有.blend文件
python blend2glb.py -b input_folder/ -o output_folder/

# 批量转换并包含动画
python blend2glb.py -b models/ -o exports/ --animations -v
```

### 查看文件信息

```bash
# 查看.blend文件的基本信息
python blend2glb.py --info model.blend

# 查看详细信息（包括所有对象、网格、材质等）
python blend2glb.py --info model.blend -v
```

### 导出选项

```bash
# 材质和纹理
--materials         # 导出材质（默认）
--no-materials      # 不导出材质

# 几何数据
--uvs              # 导出UV坐标（默认）
--no-uvs           # 不导出UV坐标
--normals          # 导出法线（默认）
--no-normals       # 不导出法线
--colors           # 导出顶点颜色（默认）
--no-colors        # 不导出顶点颜色

# 场景元素
--animations       # 导出动画
--cameras          # 导出相机
--lights           # 导出灯光

# 修改器和变换
--apply-modifiers      # 应用修改器（默认）
--no-apply-modifiers   # 不应用修改器

# 过滤选项
--selection        # 仅导出选中的对象
--visible          # 仅导出可见的对象
--renderable       # 仅导出可渲染的对象
--active-collection # 仅导出活动集合

# 其他
-v, --verbose      # 显示详细输出
--blender-path     # 指定Blender可执行文件路径
```

## 💡 使用示例

### 示例1: 游戏资产导出

```bash
# 导出用于游戏引擎的模型（无动画）
python blend2glb.py character.blend -o character.glb \
  --apply-modifiers \
  --no-cameras \
  --no-lights
```

### 示例2: 动画导出

```bash
# 导出带动画的角色
python blend2glb.py animated_character.blend -o character_anim.glb \
  --animations \
  --apply-modifiers
```

### 示例3: 完整场景导出

```bash
# 导出完整场景（包含相机和灯光）
python blend2glb.py scene.blend -o scene_complete.glb \
  --animations \
  --cameras \
  --lights \
  --materials
```

### 示例4: 批量处理工作流

```bash
# 批量转换所有资产
python blend2glb.py -b assets/blend_files/ -o assets/glb_files/ \
  --apply-modifiers \
  --materials \
  -v
```

## 🔧 Python API使用

您也可以在Python脚本中使用转换器：

```python
from core.converter_v2 import BlendToGLBConverter

# 初始化转换器
converter = BlendToGLBConverter()

# 检查是否可用
if converter.is_available():
    # 基本转换
    success = converter.convert(
        input_path="model.blend",
        output_path="model.glb"
    )
    
    # 带选项的转换
    success = converter.convert(
        input_path="animated.blend",
        output_path="animated.glb",
        export_materials=True,
        export_animations=True,
        verbose=True
    )
    
    # 批量转换
    results = converter.batch_convert(
        input_dir="input_folder/",
        output_dir="output_folder/",
        export_animations=True
    )
    
    # 获取文件信息
    info = converter.get_info("model.blend")
    print(f"对象数量: {len(info['objects'])}")
    print(f"网格数量: {len(info['meshes'])}")
```

## 📊 输出示例

### 单文件转换输出
```
✓ 找到Blender: /Applications/Blender.app/Contents/MacOS/Blender
输入文件: model.blend
输出文件: model.glb
------------------------------------------------------------
正在转换: model.blend
输出路径: /path/to/model.glb
Blender version: 4.3.0
Scene: Scene
Objects in scene: 5
  - Cube (MESH)
  - Camera (CAMERA)
  - Light (LIGHT)
  - Suzanne (MESH)
  - Plane (MESH)
✓ 转换成功！
  输出文件: model.glb
  文件大小: 45,678 字节 (44.61 KB)

你可以使用以下工具查看GLB文件:
  - 在线查看: https://gltf-viewer.donmccurdy.com/
  - Blender: File -> Import -> glTF 2.0
  - Three.js, Babylon.js等WebGL框架
```

### 批量转换输出
```
批量转换模式
输入目录: models/
输出目录: exports/
------------------------------------------------------------
找到 3 个文件
============================================================

[1/3] character.blend
正在转换: character.blend
✓ 转换成功！

[2/3] weapon.blend
正在转换: weapon.blend
✓ 转换成功！

[3/3] building.blend
正在转换: building.blend
✓ 转换成功！

============================================================
转换总结:
  成功: 3/3
  失败: 0/3
```

### 文件信息输出
```
正在读取文件信息: model.blend

============================================================
文件: model.blend
============================================================
Blender版本: 4.3.0
场景名称: Scene

统计信息:
  对象数量: 5
  网格数量: 3
  材质数量: 2
  纹理数量: 1
  动画数量: 0

对象列表:
  [✓] Camera (CAMERA)
  [✓] Light (LIGHT)
  [✓] Cube (MESH) - 8 顶点, 6 面
  [✓] Suzanne (MESH) - 507 顶点, 500 面
  [✓] Plane (MESH) - 4 顶点, 1 面
============================================================
```

## 🎯 常见问题

### Q: 转换器找不到Blender怎么办？

A: 可以手动指定Blender路径：
```bash
python blend2glb.py input.blend -o output.glb --blender-path /path/to/blender
```

### Q: 转换的GLB文件可以在哪里使用？

A: GLB文件是glTF 2.0的二进制格式，可以在以下地方使用：
- Three.js、Babylon.js等WebGL框架
- Unity、Unreal Engine等游戏引擎
- Sketchfab、Poly等3D资产平台
- AR/VR应用
- 在线3D查看器

### Q: 转换后的文件大小如何优化？

A: 可以尝试以下方法：
```bash
# 不导出不需要的内容
python blend2glb.py input.blend -o output.glb \
  --no-cameras \
  --no-lights \
  --no-animations

# 在Blender中优化模型
# - 减少多边形数量
# - 压缩纹理
# - 删除不需要的顶点组和UV层
```

### Q: 支持哪些Blender版本？

A: 支持Blender 3.0及以上版本。推荐使用最新的稳定版本以获得最佳兼容性。

### Q: 可以在没有图形界面的服务器上使用吗？

A: 可以！转换器使用Blender的`--background`模式，不需要图形界面。

## 🔄 从旧版本迁移

如果您之前使用的是旧版本的转换器（手动解析.blend文件的版本），请注意以下变化：

### 主要改进

1. **准确性** - 新版本使用Blender作为后端，转换结果100%准确
2. **完整性** - 支持所有Blender特性，不会丢失数据
3. **可靠性** - 不再生成假的立方体或回退几何体

### 使用变化

旧版本:
```bash
python blend_to_glb.py input.blend -o output.glb
```

新版本:
```bash
python blend2glb.py input.blend -o output.glb
```

### API变化

旧版本:
```python
from blend_to_glb import convert_file
convert_file("input.blend", "output.glb")
```

新版本:
```python
from core.converter_v2 import BlendToGLBConverter

converter = BlendToGLBConverter()
converter.convert("input.blend", "output.glb")
```

## 🛠️ 技术细节

### 工作原理

1. **自动检测Blender** - 在常见路径中查找Blender安装
2. **生成Python脚本** - 创建使用Blender API的转换脚本
3. **后台执行** - 在后台模式下运行Blender（无需GUI）
4. **调用导出器** - 使用Blender内置的glTF 2.0导出器
5. **返回结果** - 检查输出文件并报告结果

### 项目结构

```
blend_to_glb_converter/
├── blend2glb.py                 # 新的主入口脚本
├── core/
│   ├── blender_based_converter.py  # 基于Blender的转换引擎
│   ├── converter_v2.py             # 改进的转换器类
│   ├── converter.py                # 旧的转换器（已废弃）
│   └── blend_reader.py             # 旧的blend文件读取器（已废弃）
├── README_CN.md                 # 中文文档
├── README.md                    # 英文文档
└── test_data/                   # 测试文件
```

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎贡献！如果您发现问题或有改进建议，请：

1. Fork 这个仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## 📞 支持

如果您遇到问题或有疑问：

1. 查看本文档的常见问题部分
2. 在GitHub上提交Issue
3. 查看Blender的glTF导出文档

## 🙏 致谢

- Blender Foundation - 提供了强大的3D创作工具和GLB导出功能
- glTF工作组 - 定义和维护glTF格式规范
- 所有贡献者和用户

## 📈 版本历史

### v2.0.0 (2025-10-29)
- ✨ 重大更新：使用Blender作为后端引擎
- ✅ 100%准确的转换结果
- ✅ 支持所有Blender特性
- ✅ 新增文件信息查看功能
- ✅ 改进的命令行界面
- ✅ 更好的错误处理和用户反馈

### v1.0.0 (之前)
- ❌ 手动解析.blend文件（不准确）
- ❌ 经常生成假的几何体
- ❌ 功能有限

---

**享受使用Blend2GLB！** 🎉

如果这个工具对您有帮助，请给我们一个⭐Star！



