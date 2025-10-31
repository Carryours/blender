#!/usr/bin/env python3
"""
基于Blender的.blend到GLB转换器

这个模块使用Blender作为后端引擎来进行转换，确保转换结果100%准确。
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import tempfile
import logging


# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BlenderNotFoundError(Exception):
    """当系统中未找到Blender时抛出的异常"""
    pass


class ConversionError(Exception):
    """转换过程中发生错误时抛出的异常"""
    pass


class BlenderBasedConverter:
    """
    使用Blender作为后端的转换器
    
    这个类会自动检测系统中的Blender安装，并使用Blender的Python API
    来实现.blend文件到GLB格式的转换。
    
    Attributes:
        blender_path (str): Blender可执行文件的路径
        
    Example:
        >>> converter = BlenderBasedConverter()
        >>> success = converter.convert("input.blend", "output.glb")
        >>> if success:
        ...     print("转换成功!")
    """
    
    # 支持的Blender版本范围
    MIN_BLENDER_VERSION = (3, 0, 0)
    SUPPORTED_PLATFORMS = ['darwin', 'win32', 'linux']
    
    def __init__(self, blender_path: Optional[str] = None):
        """
        初始化转换器
        
        Args:
            blender_path: Blender可执行文件的路径。如果为None，将自动检测。
            
        Raises:
            BlenderNotFoundError: 当未找到Blender安装时
        """
        self.blender_path = blender_path or self._find_blender()
        if not self.blender_path:
            raise BlenderNotFoundError(
                "未找到Blender安装。请安装Blender或指定blender_path参数。\n"
                "下载地址: https://www.blender.org/download/"
            )
        
        logger.info(f"✓ 找到Blender: {self.blender_path}")
        
    def _find_blender(self) -> Optional[str]:
        """
        自动检测系统中的Blender安装
        
        Returns:
            Blender可执行文件的路径，如果未找到则返回None
        """
        platform_paths = self._get_platform_specific_paths()
        
        # 检查常见路径
        for path in platform_paths:
            if os.path.isfile(path):
                logger.debug(f"在路径中找到Blender: {path}")
                return path
        
        # 尝试从PATH环境变量中查找
        return self._find_blender_in_path()
    
    def _get_platform_specific_paths(self) -> List[str]:
        """获取特定平台的Blender安装路径"""
        if sys.platform == 'darwin':  # macOS
            return self._get_macos_paths()
        elif sys.platform == 'win32':  # Windows
            return self._get_windows_paths()
        else:  # Linux
            return self._get_linux_paths()
    
    def _get_macos_paths(self) -> List[str]:
        """获取macOS平台的Blender路径"""
        versions = ['4.3', '4.2', '4.1', '4.0', '3.6', '3.5', '3.4', '3.3']
        paths = ['/Applications/Blender.app/Contents/MacOS/Blender']
        
        # 添加版本特定的路径
        for version in versions:
            paths.append(f'/Applications/Blender {version}.app/Contents/MacOS/Blender')
        
        # 添加用户目录路径
        paths.append(os.path.expanduser('~/Applications/Blender.app/Contents/MacOS/Blender'))
        
        return paths
    
    def _get_windows_paths(self) -> List[str]:
        """获取Windows平台的Blender路径"""
        program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
        program_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
        
        versions = ['4.3', '4.2', '4.1', '4.0', '3.6']
        paths = [f'{program_files}\\Blender Foundation\\Blender\\blender.exe']
        
        # 添加版本特定的路径
        for version in versions:
            paths.append(f'{program_files}\\Blender Foundation\\Blender {version}\\blender.exe')
        
        # 添加x86路径
        paths.append(f'{program_files_x86}\\Blender Foundation\\Blender\\blender.exe')
        
        return paths
    
    def _get_linux_paths(self) -> List[str]:
        """获取Linux平台的Blender路径"""
        return [
            '/usr/bin/blender',
            '/usr/local/bin/blender',
            '/snap/bin/blender',
            os.path.expanduser('~/blender/blender'),
            '/opt/blender/blender',
        ]
    
    def _find_blender_in_path(self) -> Optional[str]:
        """在PATH环境变量中查找Blender"""
        try:
            cmd = ['which', 'blender'] if sys.platform != 'win32' else ['where', 'blender']
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                path = result.stdout.strip().split('\n')[0]
                if os.path.isfile(path):
                    logger.debug(f"在PATH中找到Blender: {path}")
                    return path
        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            logger.debug(f"在PATH中查找Blender失败: {e}")
        
        return None
    
    def convert(
        self,
        input_path: str,
        output_path: str,
        export_materials: bool = True,
        export_animations: bool = False,
        export_cameras: bool = False,
        export_lights: bool = False,
        export_uvs: bool = True,
        export_normals: bool = True,
        export_colors: bool = True,
        apply_modifiers: bool = True,
        use_selection: bool = False,
        use_visible: bool = False,
        use_renderable: bool = False,
        use_active_collection: bool = False,
        export_extras: bool = False,
        export_yup: bool = True,
        verbose: bool = False
    ) -> bool:
        """
        将.blend文件转换为GLB格式
        
        Args:
            input_path: 输入的.blend文件路径
            output_path: 输出的.glb文件路径
            export_materials: 导出材质
            export_animations: 导出动画
            export_cameras: 导出相机
            export_lights: 导出灯光
            export_uvs: 导出UV坐标
            export_normals: 导出法线
            export_colors: 导出顶点颜色
            apply_modifiers: 应用修改器
            use_selection: 仅导出选中的对象
            use_visible: 仅导出可见的对象
            use_renderable: 仅导出可渲染的对象
            use_active_collection: 仅导出活动集合
            export_extras: 导出自定义属性
            export_yup: 使用Y-up坐标系统（推荐用于游戏引擎）
            verbose: 显示详细输出
            
        Returns:
            转换是否成功
            
        Raises:
            FileNotFoundError: 输入文件不存在
            ValueError: 输入文件格式不正确
            ConversionError: 转换过程中出现错误
        """
        try:
            # 验证输入和准备输出
            input_path, output_path = self._validate_and_prepare_paths(input_path, output_path)
            
            # 创建转换脚本
            script_path = self._create_conversion_script(
                str(output_path),
                export_materials=export_materials,
                export_animations=export_animations,
                export_cameras=export_cameras,
                export_lights=export_lights,
                export_uvs=export_uvs,
                export_normals=export_normals,
                export_colors=export_colors,
                apply_modifiers=apply_modifiers,
                use_selection=use_selection,
                use_visible=use_visible,
                use_renderable=use_renderable,
                use_active_collection=use_active_collection,
                export_extras=export_extras,
                export_yup=export_yup
            )
            
            try:
                # 执行转换
                success = self._execute_conversion(input_path, script_path, output_path, verbose)
                return success
                
            finally:
                # 清理临时脚本文件
                self._cleanup_temp_file(script_path)
                
        except (FileNotFoundError, ValueError) as e:
            logger.error(f"输入验证失败: {e}")
            raise
        except Exception as e:
            logger.error(f"转换过程中出现未预期的错误: {e}")
            raise ConversionError(f"转换失败: {e}") from e
    
    def _validate_and_prepare_paths(self, input_path: str, output_path: str) -> Tuple[Path, Path]:
        """验证输入文件并准备输出路径"""
        # 验证输入文件
        input_path = Path(input_path).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"输入文件不存在: {input_path}")
        
        if not input_path.suffix.lower() == '.blend':
            raise ValueError(f"输入文件必须是.blend文件: {input_path}")
        
        # 准备输出路径
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"输入文件: {input_path}")
        logger.info(f"输出路径: {output_path}")
        
        return input_path, output_path
    
    def _create_conversion_script(self, output_path: str, **export_options) -> str:
        """创建转换脚本并返回临时文件路径"""
        conversion_script = self._generate_conversion_script(output_path, **export_options)
        
        # 创建临时脚本文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(conversion_script)
            script_path = f.name
        
        logger.debug(f"创建临时脚本: {script_path}")
        return script_path
    
    def _execute_conversion(
        self, 
        input_path: Path, 
        script_path: str, 
        output_path: Path, 
        verbose: bool
    ) -> bool:
        """执行Blender转换命令"""
        logger.info(f"开始转换: {input_path.name}")
        
        cmd = [
            self.blender_path,
            str(input_path),
            '--background',
            '--python', script_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            return self._process_conversion_result(result, output_path, verbose)
            
        except subprocess.TimeoutExpired:
            logger.error("转换超时（超过5分钟）")
            return False
        except Exception as e:
            logger.error(f"执行Blender命令时出错: {e}")
            return False
    
    def _process_conversion_result(
        self, 
        result: subprocess.CompletedProcess, 
        output_path: Path, 
        verbose: bool
    ) -> bool:
        """处理转换结果"""
        if verbose:
            logger.info("=== Blender输出 ===")
            logger.info(result.stdout)
            if result.stderr:
                logger.warning("=== Blender错误 ===")
                logger.warning(result.stderr)
        
        # 检查是否成功
        if result.returncode == 0 and output_path.exists():
            file_size = output_path.stat().st_size
            logger.info(f"✓ 转换成功！")
            logger.info(f"  输出文件: {output_path}")
            logger.info(f"  文件大小: {file_size:,} 字节 ({file_size / 1024:.2f} KB)")
            return True
        else:
            logger.error("✗ 转换失败")
            if not verbose:
                logger.info("使用 verbose=True 参数查看详细错误信息")
            if result.stderr:
                logger.error(f"Blender错误: {result.stderr}")
            return False
    
    def _cleanup_temp_file(self, file_path: str) -> None:
        """清理临时文件"""
        try:
            os.unlink(file_path)
            logger.debug(f"清理临时文件: {file_path}")
        except Exception as e:
            logger.warning(f"清理临时文件失败: {e}")
    
    def _generate_conversion_script(
        self,
        output_path: str,
        **export_options
    ) -> str:
        """
        生成Blender Python脚本用于转换
        
        Args:
            output_path: 输出文件路径
            **export_options: 导出选项
            
        Returns:
            Python脚本内容
        """
        # 将选项转换为Python字典格式以便在脚本中使用
        # 不能使用JSON格式，因为JSON的true/false与Python的True/False不兼容
        options_str = repr(export_options)
        
        script = f'''
import bpy
import json
import sys

def clean_shape_keys():
    """清理无效的形态键"""
    cleaned_count = 0
    
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.data.shape_keys:
            shape_keys = obj.data.shape_keys
            key_blocks = shape_keys.key_blocks
            
            # 收集需要删除的形态键（从后往前删除以避免索引问题）
            keys_to_remove = []
            for i, key in enumerate(key_blocks):
                # 检查形态键是否有问题
                if key.name != 'Basis':  # 保留基础形态键
                    try:
                        # 尝试访问形态键数据，如果有问题会抛出异常
                        _ = key.data
                        # 检查是否有无效的relative_key
                        if hasattr(key, 'relative_key') and key.relative_key is None and key.name != 'Basis':
                            keys_to_remove.append((i, key.name))
                    except:
                        # 如果访问数据时出错，标记为需要删除
                        keys_to_remove.append((i, key.name))
            
            # 从后往前删除无效的形态键
            for index, key_name in reversed(keys_to_remove):
                try:
                    # 设置活动对象
                    bpy.context.view_layer.objects.active = obj
                    obj.select_set(True)
                    
                    # 设置活动形态键索引
                    obj.active_shape_key_index = index
                    
                    # 删除形态键
                    bpy.ops.object.shape_key_remove(all=False)
                    cleaned_count += 1
                    print(f"已清理无效形态键: {{obj.name}}.{{key_name}}")
                except Exception as e:
                    print(f"清理形态键 {{key_name}} 时出错: {{e}}")
    
    if cleaned_count > 0:
        print(f"总共清理了 {{cleaned_count}} 个无效形态键")
    else:
        print("未发现需要清理的无效形态键")
    
    return cleaned_count

def convert_to_glb(output_path, options):
    """转换当前场景为GLB格式"""
    
    try:
        # 清理无效的形态键
        if options.get('clean_shape_keys', True):
            clean_shape_keys()
        
        # 确保所有对象都被更新
        bpy.context.view_layer.update()
        
        # 准备导出选项
        export_kwargs = {{
            'filepath': output_path,
            'export_format': 'GLB',
            'export_copyright': '',
            'export_image_format': 'AUTO',
            'export_texture_dir': '',
            'export_texcoords': options.get('export_uvs', True),
            'export_normals': options.get('export_normals', True),
            'export_draco_mesh_compression_enable': False,
            'export_tangents': False,
            'export_materials': 'EXPORT' if options.get('export_materials', True) else 'NONE',
            # 'export_colors': options.get('export_colors', True),  # 在Blender 4.5中不支持
            'export_attributes': False,
            'use_mesh_edges': False,
            'use_mesh_vertices': False,
            'export_cameras': options.get('export_cameras', False),
            'use_selection': options.get('use_selection', False),
            'use_visible': options.get('use_visible', False),
            'use_renderable': options.get('use_renderable', False),
            'use_active_collection': options.get('use_active_collection', False),
            'export_extras': options.get('export_extras', False),
            'export_yup': options.get('export_yup', True),
            'export_apply': options.get('apply_modifiers', True),
            'export_animations': options.get('export_animations', False),
            'export_frame_range': False,
            'export_frame_step': 1,
            'export_force_sampling': True,
            'export_nla_strips': True,
            'export_def_bones': False,
            'export_optimize_animation_size': True,
            'export_anim_single_armature': True,
            'export_reset_pose_bones': True,
            'export_current_frame': False,
            'export_skins': True,
            'export_all_influences': False,
            'export_morph': True,
            'export_morph_normal': True,
            'export_morph_tangent': False,
            'export_lights': options.get('export_lights', False),
        }}
        
        # 调用GLB导出器
        bpy.ops.export_scene.gltf(**export_kwargs)
        
        print(f"Successfully exported to: {{output_path}}")
        return True
        
    except Exception as e:
        print(f"Export failed: {{e}}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

# 主执行
if __name__ == "__main__":
    output_path = r"{output_path}"
    options = {options_str}
    
    print(f"Blender version: {{bpy.app.version_string}}")
    print(f"Scene: {{bpy.context.scene.name}}")
    print(f"Objects in scene: {{len(bpy.data.objects)}}")
    
    # 显示场景中的对象
    for obj in bpy.data.objects:
        print(f"  - {{obj.name}} ({{obj.type}})")
    
    # 执行转换
    success = convert_to_glb(output_path, options)
    
    if not success:
        sys.exit(1)
'''
        
        return script
    
    def batch_convert(
        self,
        input_dir: str,
        output_dir: str,
        pattern: str = "*.blend",
        **export_options
    ) -> Dict[str, bool]:
        """
        批量转换目录中的.blend文件
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            pattern: 文件匹配模式
            **export_options: 导出选项
            
        Returns:
            转换结果字典 {文件名: 是否成功}
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {}
        blend_files = list(input_path.glob(pattern))
        
        if not blend_files:
            print(f"在 {input_dir} 中未找到匹配 {pattern} 的文件")
            return results
        
        print(f"找到 {len(blend_files)} 个文件")
        print("=" * 60)
        
        for i, blend_file in enumerate(blend_files, 1):
            print(f"\n[{i}/{len(blend_files)}] {blend_file.name}")
            
            output_file = output_path / blend_file.with_suffix('.glb').name
            
            try:
                success = self.convert(
                    str(blend_file),
                    str(output_file),
                    **export_options
                )
                results[blend_file.name] = success
            except Exception as e:
                print(f"✗ 错误: {e}")
                results[blend_file.name] = False
        
        # 打印总结
        print("\n" + "=" * 60)
        print("转换总结:")
        successful = sum(1 for v in results.values() if v)
        print(f"  成功: {successful}/{len(results)}")
        print(f"  失败: {len(results) - successful}/{len(results)}")
        
        return results
    
    def get_blend_info(self, input_path: str, verbose: bool = False) -> Optional[Dict[str, Any]]:
        """
        获取.blend文件的信息（不进行转换）
        
        Args:
            input_path: .blend文件路径
            verbose: 显示详细信息
            
        Returns:
            文件信息字典
        """
        input_path = Path(input_path).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"文件不存在: {input_path}")
        
        # 创建信息提取脚本
        info_script = '''
import bpy
import json
import sys

def get_blend_info():
    """提取blend文件信息"""
    info = {
        'blender_version': bpy.app.version_string,
        'scene_name': bpy.context.scene.name,
        'objects': [],
        'meshes': [],
        'materials': [],
        'textures': [],
        'animations': []
    }
    
    # 对象信息
    for obj in bpy.data.objects:
        obj_info = {
            'name': obj.name,
            'type': obj.type,
            'visible': not obj.hide_viewport,
            'location': list(obj.location),
            'rotation': list(obj.rotation_euler),
            'scale': list(obj.scale)
        }
        
        if obj.type == 'MESH' and obj.data:
            obj_info['vertices'] = len(obj.data.vertices)
            obj_info['faces'] = len(obj.data.polygons)
            obj_info['edges'] = len(obj.data.edges)
        
        info['objects'].append(obj_info)
    
    # 网格信息
    for mesh in bpy.data.meshes:
        mesh_info = {
            'name': mesh.name,
            'vertices': len(mesh.vertices),
            'faces': len(mesh.polygons),
            'edges': len(mesh.edges),
            'materials': len(mesh.materials)
        }
        info['meshes'].append(mesh_info)
    
    # 材质信息
    for mat in bpy.data.materials:
        mat_info = {
            'name': mat.name,
            'use_nodes': mat.use_nodes
        }
        info['materials'].append(mat_info)
    
    # 纹理信息
    for tex in bpy.data.images:
        tex_info = {
            'name': tex.name,
            'size': list(tex.size),
            'filepath': tex.filepath
        }
        info['textures'].append(tex_info)
    
    # 动画信息
    for action in bpy.data.actions:
        anim_info = {
            'name': action.name,
            'frame_range': [action.frame_range[0], action.frame_range[1]],
            'fcurves': len(action.fcurves)
        }
        info['animations'].append(anim_info)
    
    return info

# 主执行
if __name__ == "__main__":
    info = get_blend_info()
    print("BLEND_INFO_START")
    print(json.dumps(info, indent=2))
    print("BLEND_INFO_END")
'''
        
        # 创建临时脚本文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(info_script)
            script_path = f.name
        
        try:
            cmd = [
                self.blender_path,
                str(input_path),
                '--background',
                '--python', script_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if verbose:
                print(result.stdout)
            
            # 提取JSON信息
            stdout = result.stdout
            if 'BLEND_INFO_START' in stdout and 'BLEND_INFO_END' in stdout:
                start = stdout.index('BLEND_INFO_START') + len('BLEND_INFO_START')
                end = stdout.index('BLEND_INFO_END')
                json_str = stdout[start:end].strip()
                return json.loads(json_str)
            else:
                print("无法提取文件信息")
                return None
                
        except Exception as e:
            print(f"获取信息失败: {e}")
            return None
        finally:
            try:
                os.unlink(script_path)
            except:
                pass


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='基于Blender的.blend到GLB转换器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 基本转换
  python blender_based_converter.py input.blend -o output.glb
  
  # 批量转换
  python blender_based_converter.py -b input_dir/ -o output_dir/
  
  # 查看文件信息
  python blender_based_converter.py -i model.blend
  
  # 转换时包含动画和灯光
  python blender_based_converter.py input.blend -o output.glb --animations --lights
        '''
    )
    
    parser.add_argument('input', nargs='?', help='输入的.blend文件或目录')
    parser.add_argument('-o', '--output', help='输出的.glb文件或目录')
    parser.add_argument('-b', '--batch', action='store_true', help='批量转换模式')
    parser.add_argument('-i', '--info', action='store_true', help='仅显示文件信息（不转换）')
    parser.add_argument('--blender-path', help='Blender可执行文件路径')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细输出')
    
    # 导出选项
    export_group = parser.add_argument_group('导出选项')
    export_group.add_argument('--no-materials', action='store_true', help='不导出材质')
    export_group.add_argument('--animations', action='store_true', help='导出动画')
    export_group.add_argument('--cameras', action='store_true', help='导出相机')
    export_group.add_argument('--lights', action='store_true', help='导出灯光')
    export_group.add_argument('--no-uvs', action='store_true', help='不导出UV')
    export_group.add_argument('--no-normals', action='store_true', help='不导出法线')
    export_group.add_argument('--no-apply-modifiers', action='store_true', help='不应用修改器')
    
    args = parser.parse_args()
    
    if not args.input:
        parser.print_help()
        return 1
    
    try:
        # 初始化转换器
        converter = BlenderBasedConverter(blender_path=args.blender_path)
        
        # 信息模式
        if args.info:
            info = converter.get_blend_info(args.input, verbose=args.verbose)
            if info:
                print(json.dumps(info, indent=2, ensure_ascii=False))
                return 0
            return 1
        
        # 检查输出参数
        if not args.output:
            print("错误: 需要指定输出路径 (-o/--output)")
            return 1
        
        # 准备导出选项
        export_options = {
            'export_materials': not args.no_materials,
            'export_animations': args.animations,
            'export_cameras': args.cameras,
            'export_lights': args.lights,
            'export_uvs': not args.no_uvs,
            'export_normals': not args.no_normals,
            'apply_modifiers': not args.no_apply_modifiers,
            'verbose': args.verbose
        }
        
        # 批量模式
        if args.batch:
            results = converter.batch_convert(
                args.input,
                args.output,
                **export_options
            )
            return 0 if any(results.values()) else 1
        
        # 单文件模式
        else:
            success = converter.convert(
                args.input,
                args.output,
                **export_options
            )
            return 0 if success else 1
            
    except Exception as e:
        print(f"错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())



