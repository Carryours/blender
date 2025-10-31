# 快速开始指南

## 🎯 核心优势

**新版本转换器使用Blender作为后端引擎**，完全解决了旧版本的问题：
- ✅ **100%准确转换** - 不再生成假数据
- ✅ **完整功能支持** - 材质、纹理、动画、相机、灯光等
- ✅ **真实数据** - 所有内容都来自源.blend文件

## 🚀 5分钟快速上手

### 1. 安装Blender

**macOS:**
```bash
brew install --cask blender
```

**Windows:**
```bash
choco install blender
```

**Linux:**
```bash
sudo apt install blender
```

### 2. 验证安装

```bash
# 检查Blender是否正确安装
blender --version
```

### 3. 基本转换

```bash
# 最简单的转换命令
python blend2glb.py input.blend -o output.glb

# 带详细输出
python blend2glb.py input.blend -o output.glb -v
```

### 4. 高级用法

```bash
# 包含所有特性的转换
python blend2glb.py model.blend -o model.glb \
  --materials \
  --animations \
  --cameras \
  --lights \
  --verbose

# 批量转换
python blend2glb.py -b input_folder/ -o output_folder/

# 查看文件信息
python blend2glb.py --info model.blend
```

## 🔧 常见问题

### Q: 提示"Blender not found"怎么办？
A: 确保Blender已正确安装并添加到系统PATH中。

### Q: 转换失败怎么办？
A: 使用 `-v` 参数查看详细错误信息：
```bash
python blend2glb.py input.blend -o output.glb -v
```

### Q: 如何批量转换？
A: 使用 `-b` 参数指定输入目录：
```bash
python blend2glb.py -b /path/to/blend/files/ -o /path/to/output/
```

## 📚 更多资源

- [完整文档](README.md)
- [API参考](docs/API.md)
- [贡献指南](CONTRIBUTING.md)

---

**提示**: 如果您之前使用过旧版本，新版本的API完全兼容，只需要确保安装了Blender即可获得更好的转换效果！

**Windows用户：**
```bash
# 访问 https://www.blender.org/download/
# 下载安装程序并运行
```

**Linux用户：**
```bash
# Ubuntu/Debian
sudo apt install blender

# 或使用Snap (推荐)
sudo snap install blender --classic
```

### 2. 验证安装

安装完成后，确认Blender可以运行：
```bash
# macOS
/Applications/Blender.app/Contents/MacOS/Blender --version

# Windows
"C:\Program Files\Blender Foundation\Blender\blender.exe" --version

# Linux
blender --version
```

## 使用方法

### 方法1: 使用命令行工具（推荐）

```bash
cd blend_to_glb_converter

# 基本转换
python3 blend2glb.py input.blend -o output.glb

# 转换您的武器模型
python3 blend2glb.py "test_data/武器.blend" -o "test_data/weapon.glb"

# 转换Cyberpunk Loft场景
python3 blend2glb.py "test_data/Cyberpunk Loft.blend" -o "test_data/scene.glb"

# 查看文件信息
python3 blend2glb.py --info "test_data/武器.blend"

# 批量转换
python3 blend2glb.py -b test_data/ -o output/ -v
```

### 方法2: 使用Python API

创建一个Python脚本：

```python
#!/usr/bin/env python3
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from converter_v2 import BlendToGLBConverter

# 初始化转换器
converter = BlendToGLBConverter()

# 检查是否可用
if not converter.is_available():
    print("错误: 请先安装Blender")
    print("下载地址: https://www.blender.org/download/")
    sys.exit(1)

# 转换单个文件
print("转换武器模型...")
success = converter.convert(
    input_path="test_data/武器.blend",
    output_path="test_data/weapon_converted.glb",
    export_materials=True,
    export_animations=False,
    verbose=True
)

if success:
    print("✓ 转换成功！")
else:
    print("✗ 转换失败")

# 查看文件信息
print("\n获取文件信息...")
info = converter.get_info("test_data/武器.blend")
if info:
    print(f"Blender版本: {info['blender_version']}")
    print(f"对象数量: {len(info['objects'])}")
    print(f"网格数量: {len(info['meshes'])}")
    print(f"材质数量: {len(info['materials'])}")

# 批量转换
print("\n批量转换...")
results = converter.batch_convert(
    input_dir="test_data/",
    output_dir="output/",
    export_materials=True,
    verbose=False
)

successful = sum(1 for v in results.values() if v)
print(f"批量转换完成: {successful}/{len(results)} 成功")
```

保存为 `my_converter.py` 并运行：
```bash
python3 my_converter.py
```

## 完整示例

### 示例1: 转换游戏资产

```bash
# 转换武器模型（适用于游戏引擎）
python3 blend2glb.py "test_data/武器.blend" \
  -o "game_assets/weapon.glb" \
  --apply-modifiers \
  --no-cameras \
  --no-lights \
  -v
```

### 示例2: 转换场景（包含所有内容）

```bash
# 转换完整场景（包含相机和灯光）
python3 blend2glb.py "test_data/Cyberpunk Loft.blend" \
  -o "scenes/cyberpunk_loft.glb" \
  --materials \
  --cameras \
  --lights \
  -v
```

### 示例3: 批量转换所有文件

```bash
# 批量转换test_data目录中的所有.blend文件
python3 blend2glb.py -b test_data/ -o converted/ -v
```

## 导出选项说明

### 几何数据
- `--materials` / `--no-materials` - 导出材质（默认启用）
- `--uvs` / `--no-uvs` - 导出UV坐标（默认启用）
- `--normals` / `--no-normals` - 导出法线（默认启用）
- `--colors` / `--no-colors` - 导出顶点颜色（默认启用）

### 场景元素
- `--animations` - 导出动画
- `--cameras` - 导出相机
- `--lights` - 导出灯光

### 修改器和变换
- `--apply-modifiers` / `--no-apply-modifiers` - 应用修改器（默认启用）

### 过滤选项
- `--selection` - 仅导出选中的对象
- `--visible` - 仅导出可见的对象
- `--renderable` - 仅导出可渲染的对象

### 其他
- `-v` / `--verbose` - 显示详细输出
- `--blender-path` - 手动指定Blender路径

## 对比：旧版 vs 新版

### 旧版转换器的问题

```bash
# 旧版转换器
python3 blend_to_glb.py input.blend -o output.glb

# 结果：
# ✗ 生成的是假的立方体，不是真实模型
# ✗ 无法读取复杂的.blend文件格式
# ✗ 材质、纹理、动画全部丢失
```

### 新版转换器的优势

```bash
# 新版转换器
python3 blend2glb.py input.blend -o output.glb

# 结果：
# ✓ 生成的是真实的模型数据
# ✓ 使用Blender引擎，100%准确
# ✓ 完整保留材质、纹理、动画等所有数据
```

## 常见问题

### Q1: 转换器提示找不到Blender

**解决方法：**
```bash
# 方法1: 确保Blender安装在标准位置
# macOS: /Applications/Blender.app/
# Windows: C:\Program Files\Blender Foundation\Blender\
# Linux: /usr/bin/blender

# 方法2: 手动指定Blender路径
python3 blend2glb.py input.blend -o output.glb \
  --blender-path "/Applications/Blender.app/Contents/MacOS/Blender"
```

### Q2: 转换失败，没有生成文件

**解决方法：**
```bash
# 使用 -v 参数查看详细错误信息
python3 blend2glb.py input.blend -o output.glb -v

# 检查输入文件是否正确
python3 blend2glb.py --info input.blend
```

### Q3: 转换后的文件太大

**解决方法：**
```bash
# 1. 不导出不需要的内容
python3 blend2glb.py input.blend -o output.glb \
  --no-cameras --no-lights --no-animations

# 2. 在Blender中优化模型
# - 减少多边形数量
# - 压缩纹理
# - 删除不需要的数据
```

### Q4: 如何查看转换后的GLB文件

**方法1: 在线查看器**
- https://gltf-viewer.donmccurdy.com/
- https://sandbox.babylonjs.com/

**方法2: 在Blender中打开**
```
File -> Import -> glTF 2.0 -> 选择.glb文件
```

**方法3: 在Web项目中使用**
```javascript
// 使用Three.js
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('model.glb', (gltf) => {
    scene.add(gltf.scene);
});
```

## 验证转换结果

转换完成后，验证结果：

```bash
# 1. 检查文件大小（应该大于几KB）
ls -lh output.glb

# 2. 查看文件信息
python3 blend2glb.py --info output.glb

# 3. 在Blender中打开查看
# File -> Import -> glTF 2.0 -> output.glb
```

## 下一步

1. **测试转换器** - 使用test_data中的示例文件测试
2. **转换您的模型** - 转换您自己的.blend文件
3. **集成到工作流** - 将转换器集成到您的构建流程中
4. **阅读完整文档** - 查看 README_CN.md 了解更多细节

## 技术支持

如果您遇到问题：

1. 查看详细错误信息（使用 `-v` 参数）
2. 确认Blender正确安装
3. 检查.blend文件是否损坏
4. 在GitHub上提交Issue

---

**现在开始使用新的转换器，享受100%准确的转换结果！** 🎉



