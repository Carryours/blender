"""
改进的Blender到GLB转换器 V2

这个版本使用Blender作为后端引擎，确保转换结果完全准确。
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blender_based_converter import BlenderBasedConverter


class BlendToGLBConverter:
    """
    改进的.blend到GLB转换器
    
    这个版本使用Blender作为后端引擎，保证转换质量和准确性。
    
    特性:
    - ✅ 100%准确的转换（使用Blender内置导出器）
    - ✅ 支持所有Blender特性（材质、纹理、动画等）
    - ✅ 自动检测Blender安装
    - ✅ 批量转换支持
    - ✅ 详细的进度和错误报告
    """
    
    def __init__(self, blender_path: Optional[str] = None):
        """
        初始化转换器
        
        Args:
            blender_path: Blender可执行文件路径（可选）
        """
        try:
            self.backend = BlenderBasedConverter(blender_path=blender_path)
            self.available = True
        except RuntimeError as e:
            print(f"警告: {e}")
            self.backend = None
            self.available = False
    
    def is_available(self) -> bool:
        """检查转换器是否可用"""
        return self.available
    
    def convert(
        self,
        input_path: str,
        output_path: str,
        export_materials: bool = True,
        export_animations: bool = False,
        export_cameras: bool = False,
        export_lights: bool = False,
        apply_modifiers: bool = True,
        verbose: bool = False,
        **kwargs
    ) -> bool:
        """
        转换.blend文件为GLB格式
        
        Args:
            input_path: 输入.blend文件路径
            output_path: 输出.glb文件路径
            export_materials: 是否导出材质
            export_animations: 是否导出动画
            export_cameras: 是否导出相机
            export_lights: 是否导出灯光
            apply_modifiers: 是否应用修改器
            verbose: 是否显示详细输出
            **kwargs: 其他导出选项
            
        Returns:
            转换是否成功
        """
        if not self.available:
            print("错误: 转换器不可用。请安装Blender。")
            print("下载地址: https://www.blender.org/download/")
            return False
        
        try:
            return self.backend.convert(
                input_path=input_path,
                output_path=output_path,
                export_materials=export_materials,
                export_animations=export_animations,
                export_cameras=export_cameras,
                export_lights=export_lights,
                apply_modifiers=apply_modifiers,
                verbose=verbose,
                **kwargs
            )
        except Exception as e:
            print(f"转换失败: {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            return False
    
    def batch_convert(
        self,
        input_dir: str,
        output_dir: str,
        pattern: str = "*.blend",
        **options
    ) -> Dict[str, bool]:
        """
        批量转换目录中的.blend文件
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            pattern: 文件匹配模式（默认: *.blend）
            **options: 导出选项
            
        Returns:
            转换结果字典 {文件名: 是否成功}
        """
        if not self.available:
            print("错误: 转换器不可用。请安装Blender。")
            return {}
        
        return self.backend.batch_convert(
            input_dir=input_dir,
            output_dir=output_dir,
            pattern=pattern,
            **options
        )
    
    def get_info(self, input_path: str, verbose: bool = False) -> Optional[Dict[str, Any]]:
        """
        获取.blend文件信息
        
        Args:
            input_path: .blend文件路径
            verbose: 显示详细输出
            
        Returns:
            文件信息字典，如果失败则返回None
        """
        if not self.available:
            print("错误: 转换器不可用。请安装Blender。")
            return None
        
        return self.backend.get_blend_info(input_path, verbose=verbose)
    
    def convert_with_options(
        self,
        input_path: str,
        output_path: str,
        options: Dict[str, Any]
    ) -> bool:
        """
        使用选项字典进行转换
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            options: 导出选项字典
            
        Returns:
            转换是否成功
        """
        return self.convert(input_path, output_path, **options)
    
    # 兼容性方法（用于旧代码）
    def load_blend_data(self, filepath: str) -> Dict[str, Any]:
        """
        加载.blend文件数据（兼容性方法）
        
        Note: 这个方法用于向后兼容，实际转换时不需要调用
        """
        return self.get_info(filepath) or {}
    
    def convert_to_gltf(
        self,
        blend_data: Dict[str, Any],
        export_materials: bool = True
    ) -> Dict[str, Any]:
        """
        转换blend数据为GLTF格式（兼容性方法）
        
        Note: 新版本不需要这个中间步骤，直接使用convert()方法
        """
        return blend_data
    
    def export_glb(
        self,
        gltf_data: Dict[str, Any],
        output_path: str
    ) -> bool:
        """
        导出GLB文件（兼容性方法）
        
        Note: 新版本不需要这个方法，直接使用convert()方法
        """
        print("警告: export_glb() 是遗留方法，请使用 convert() 方法")
        return False


def print_installation_guide():
    """打印Blender安装指南"""
    print("\n" + "="*60)
    print("Blender安装指南")
    print("="*60)
    print("\n本转换器需要安装Blender才能工作。")
    print("\n下载地址: https://www.blender.org/download/")
    print("\n安装步骤:")
    print("  macOS:")
    print("    1. 下载 Blender.dmg")
    print("    2. 拖动Blender到Applications文件夹")
    print("    3. 转换器会自动检测到安装")
    print("\n  Windows:")
    print("    1. 下载 Blender安装包")
    print("    2. 运行安装程序")
    print("    3. 使用默认安装路径")
    print("\n  Linux:")
    print("    Ubuntu/Debian: sudo apt install blender")
    print("    Fedora: sudo dnf install blender")
    print("    Arch: sudo pacman -S blender")
    print("\n或者使用Snap: sudo snap install blender --classic")
    print("\n安装后，重新运行转换器即可。")
    print("="*60 + "\n")


def main():
    """测试和演示"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Blender到GLB转换器 V2',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input', help='输入.blend文件')
    parser.add_argument('-o', '--output', help='输出.glb文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('--info', action='store_true', help='仅显示文件信息')
    parser.add_argument('--animations', action='store_true', help='导出动画')
    parser.add_argument('--cameras', action='store_true', help='导出相机')
    parser.add_argument('--lights', action='store_true', help='导出灯光')
    
    args = parser.parse_args()
    
    # 初始化转换器
    converter = BlendToGLBConverter()
    
    if not converter.is_available():
        print_installation_guide()
        return 1
    
    # 信息模式
    if args.info:
        info = converter.get_info(args.input, verbose=args.verbose)
        if info:
            import json
            print(json.dumps(info, indent=2, ensure_ascii=False))
            return 0
        return 1
    
    # 转换模式
    if not args.output:
        # 自动生成输出文件名
        args.output = Path(args.input).with_suffix('.glb')
    
    success = converter.convert(
        input_path=args.input,
        output_path=args.output,
        export_animations=args.animations,
        export_cameras=args.cameras,
        export_lights=args.lights,
        verbose=args.verbose
    )
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())



