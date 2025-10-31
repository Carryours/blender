#!/usr/bin/env python3
"""
Blend2GLB - 高质量的Blender到GLB转换器

这个工具使用Blender作为后端引擎，确保100%准确的转换结果。
"""

import sys
import os
from pathlib import Path
import argparse
import json

# 添加core目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from converter_v2 import BlendToGLBConverter, print_installation_guide


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        prog='blend2glb',
        description='Blend2GLB - 高质量的Blender到GLB转换器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 基本转换
  %(prog)s input.blend -o output.glb
  
  # 转换并包含动画
  %(prog)s model.blend -o model.glb --animations
  
  # 批量转换目录中的所有文件
  %(prog)s -b input_dir/ -o output_dir/
  
  # 查看blend文件信息
  %(prog)s --info model.blend
  
  # 详细输出模式
  %(prog)s input.blend -o output.glb -v
  
  # 转换时包含所有内容（材质、动画、相机、灯光）
  %(prog)s scene.blend -o scene.glb --animations --cameras --lights

更多信息:
  GitHub: https://github.com/your-repo/blend_to_glb_converter
  文档: https://blend2glb.readthedocs.io/
        '''
    )
    
    # 输入/输出参数
    io_group = parser.add_argument_group('输入/输出')
    io_group.add_argument(
        'input',
        nargs='?',
        help='输入的.blend文件或目录'
    )
    io_group.add_argument(
        '-o', '--output',
        help='输出的.glb文件或目录'
    )
    io_group.add_argument(
        '-b', '--batch',
        action='store_true',
        help='批量转换模式（转换目录中的所有.blend文件）'
    )
    
    # 导出选项
    export_group = parser.add_argument_group('导出选项')
    export_group.add_argument(
        '--materials',
        action='store_true',
        default=True,
        help='导出材质（默认启用）'
    )
    export_group.add_argument(
        '--no-materials',
        action='store_true',
        help='不导出材质'
    )
    export_group.add_argument(
        '--animations',
        action='store_true',
        help='导出动画'
    )
    export_group.add_argument(
        '--cameras',
        action='store_true',
        help='导出相机'
    )
    export_group.add_argument(
        '--lights',
        action='store_true',
        help='导出灯光'
    )
    export_group.add_argument(
        '--uvs',
        action='store_true',
        default=True,
        help='导出UV坐标（默认启用）'
    )
    export_group.add_argument(
        '--no-uvs',
        action='store_true',
        help='不导出UV坐标'
    )
    export_group.add_argument(
        '--normals',
        action='store_true',
        default=True,
        help='导出法线（默认启用）'
    )
    export_group.add_argument(
        '--no-normals',
        action='store_true',
        help='不导出法线'
    )
    export_group.add_argument(
        '--colors',
        action='store_true',
        default=True,
        help='导出顶点颜色（默认启用）'
    )
    export_group.add_argument(
        '--no-colors',
        action='store_true',
        help='不导出顶点颜色'
    )
    export_group.add_argument(
        '--apply-modifiers',
        action='store_true',
        default=True,
        help='应用修改器（默认启用）'
    )
    export_group.add_argument(
        '--no-apply-modifiers',
        action='store_true',
        help='不应用修改器'
    )
    
    # 过滤选项
    filter_group = parser.add_argument_group('过滤选项')
    filter_group.add_argument(
        '--selection',
        action='store_true',
        help='仅导出选中的对象'
    )
    filter_group.add_argument(
        '--visible',
        action='store_true',
        help='仅导出可见的对象'
    )
    filter_group.add_argument(
        '--renderable',
        action='store_true',
        help='仅导出可渲染的对象'
    )
    filter_group.add_argument(
        '--active-collection',
        action='store_true',
        help='仅导出活动集合中的对象'
    )
    
    # 其他选项
    other_group = parser.add_argument_group('其他选项')
    other_group.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细输出'
    )
    other_group.add_argument(
        '--info',
        action='store_true',
        help='显示.blend文件信息（不进行转换）'
    )
    other_group.add_argument(
        '--blender-path',
        help='指定Blender可执行文件路径'
    )
    other_group.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2.0.0'
    )
    
    args = parser.parse_args()
    
    # 检查输入参数
    if not args.input:
        parser.print_help()
        return 0
    
    # 初始化转换器
    try:
        converter = BlendToGLBConverter(blender_path=args.blender_path)
    except Exception as e:
        print(f"初始化转换器失败: {e}")
        return 1
    
    if not converter.is_available():
        print_installation_guide()
        return 1
    
    # 信息模式
    if args.info:
        print(f"正在读取文件信息: {args.input}")
        info = converter.get_info(args.input, verbose=args.verbose)
        
        if info:
            print("\n" + "="*60)
            print(f"文件: {Path(args.input).name}")
            print("="*60)
            print(f"Blender版本: {info.get('blender_version', 'Unknown')}")
            print(f"场景名称: {info.get('scene_name', 'Unknown')}")
            print(f"\n统计信息:")
            print(f"  对象数量: {len(info.get('objects', []))}")
            print(f"  网格数量: {len(info.get('meshes', []))}")
            print(f"  材质数量: {len(info.get('materials', []))}")
            print(f"  纹理数量: {len(info.get('textures', []))}")
            print(f"  动画数量: {len(info.get('animations', []))}")
            
            # 显示对象详情
            objects = info.get('objects', [])
            if objects:
                print(f"\n对象列表:")
                for obj in objects:
                    obj_type = obj.get('type', 'UNKNOWN')
                    obj_name = obj.get('name', 'Unnamed')
                    visible = '✓' if obj.get('visible', True) else '✗'
                    print(f"  [{visible}] {obj_name} ({obj_type})", end='')
                    
                    if obj_type == 'MESH':
                        verts = obj.get('vertices', 0)
                        faces = obj.get('faces', 0)
                        print(f" - {verts:,} 顶点, {faces:,} 面")
                    else:
                        print()
            
            # 显示网格详情
            meshes = info.get('meshes', [])
            if meshes and args.verbose:
                print(f"\n网格详情:")
                for mesh in meshes:
                    mesh_name = mesh.get('name', 'Unnamed')
                    verts = mesh.get('vertices', 0)
                    faces = mesh.get('faces', 0)
                    materials = mesh.get('materials', 0)
                    print(f"  {mesh_name}:")
                    print(f"    顶点: {verts:,}")
                    print(f"    面: {faces:,}")
                    print(f"    材质: {materials}")
            
            # 显示材质列表
            materials = info.get('materials', [])
            if materials and args.verbose:
                print(f"\n材质列表:")
                for mat in materials:
                    mat_name = mat.get('name', 'Unnamed')
                    uses_nodes = '节点' if mat.get('use_nodes', False) else '传统'
                    print(f"  {mat_name} ({uses_nodes})")
            
            # 显示动画信息
            animations = info.get('animations', [])
            if animations:
                print(f"\n动画列表:")
                for anim in animations:
                    anim_name = anim.get('name', 'Unnamed')
                    frame_range = anim.get('frame_range', [0, 0])
                    fcurves = anim.get('fcurves', 0)
                    print(f"  {anim_name}")
                    print(f"    帧范围: {frame_range[0]:.0f} - {frame_range[1]:.0f}")
                    print(f"    曲线数: {fcurves}")
            
            print("="*60)
            
            # 如果使用verbose模式，输出完整JSON
            if args.verbose:
                print("\n完整信息 (JSON):")
                print(json.dumps(info, indent=2, ensure_ascii=False))
            
            return 0
        else:
            print("✗ 无法读取文件信息")
            return 1
    
    # 检查输出参数
    if not args.output:
        if args.batch:
            print("错误: 批量模式需要指定输出目录 (-o/--output)")
            return 1
        else:
            # 自动生成输出文件名
            args.output = str(Path(args.input).with_suffix('.glb'))
            print(f"自动设置输出文件: {args.output}")
    
    # 准备导出选项
    export_options = {
        'export_materials': not args.no_materials,
        'export_animations': args.animations,
        'export_cameras': args.cameras,
        'export_lights': args.lights,
        'export_uvs': not args.no_uvs,
        'export_normals': not args.no_normals,
        'export_colors': not args.no_colors,
        'apply_modifiers': not args.no_apply_modifiers,
        'use_selection': args.selection,
        'use_visible': args.visible,
        'use_renderable': args.renderable,
        'use_active_collection': args.active_collection,
        'verbose': args.verbose
    }
    
    # 批量转换模式
    if args.batch:
        print(f"批量转换模式")
        print(f"输入目录: {args.input}")
        print(f"输出目录: {args.output}")
        print("-" * 60)
        
        results = converter.batch_convert(
            input_dir=args.input,
            output_dir=args.output,
            pattern="*.blend",
            **export_options
        )
        
        if not results:
            print("✗ 未找到任何.blend文件")
            return 1
        
        # 统计结果
        successful = sum(1 for v in results.values() if v)
        failed = len(results) - successful
        
        if failed == 0:
            print("\n✓ 所有文件转换成功！")
            return 0
        else:
            print(f"\n⚠ 部分文件转换失败")
            print(f"  成功: {successful}")
            print(f"  失败: {failed}")
            return 1
    
    # 单文件转换模式
    else:
        # 验证输入文件
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"错误: 输入文件不存在: {args.input}")
            return 1
        
        if not input_path.suffix.lower() == '.blend':
            print(f"错误: 输入文件必须是.blend文件: {args.input}")
            return 1
        
        # 显示转换信息
        print(f"输入文件: {args.input}")
        print(f"输出文件: {args.output}")
        
        if args.verbose:
            print("\n导出选项:")
            for key, value in export_options.items():
                if key != 'verbose':
                    print(f"  {key}: {value}")
        
        print("-" * 60)
        
        # 执行转换
        success = converter.convert(
            input_path=args.input,
            output_path=args.output,
            **export_options
        )
        
        if success:
            output_path = Path(args.output)
            if output_path.exists():
                size = output_path.stat().st_size
                print(f"\n✓ 转换成功！")
                print(f"  输出文件: {args.output}")
                print(f"  文件大小: {size:,} 字节 ({size/1024:.2f} KB)")
                
                # 提示可以在哪里查看
                print(f"\n你可以使用以下工具查看GLB文件:")
                print(f"  - 在线查看: https://gltf-viewer.donmccurdy.com/")
                print(f"  - Blender: File -> Import -> glTF 2.0")
                print(f"  - Three.js, Babylon.js等WebGL框架")
            return 0
        else:
            print("\n✗ 转换失败")
            if not args.verbose:
                print("使用 -v/--verbose 参数查看详细错误信息")
            return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n✗ 用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



