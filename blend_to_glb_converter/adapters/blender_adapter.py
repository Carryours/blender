"""
Blender Data Adapter

Converts Blender .blend file data to standardized format for GLTF conversion.
"""

import math
from typing import Dict, List, Any, Optional
from .base_adapter import BaseDataAdapter
from core.blend_reader import SimpleBlendReader


class BlenderDataAdapter(BaseDataAdapter):
    """
    Adapter for converting Blender .blend file data to GLTF format.
    """
    
    def __init__(self):
        self.blend_data: Optional[Dict[str, Any]] = None
        self.filepath: Optional[str] = None
    
    def load_file(self, filepath: str) -> Dict[str, Any]:
        """Load and parse a .blend file"""
        self.filepath = filepath
        reader = SimpleBlendReader(filepath)
        self.blend_data = reader.read()
        return self.blend_data
    
    def get_meshes(self) -> List[Dict[str, Any]]:
        """Convert Blender mesh data to standardized format"""
        if not self.blend_data:
            return []
        
        standardized_meshes = []
        
        for i, mesh in enumerate(self.blend_data.get('meshes', [])):
            # Convert Blender mesh to standardized format
            standardized_mesh = {
                'name': mesh.get('name', f'Mesh_{i}'),
                'vertices': self._convert_vertices(mesh.get('vertices', [])),
                'faces': self._convert_faces(mesh.get('faces', [])),
                'normals': self._convert_normals(mesh.get('normals', [])),
                'uvs': self._convert_uvs(mesh.get('uvs', [])),
                'materials': mesh.get('materials', [])
            }
            standardized_meshes.append(standardized_mesh)
        
        return standardized_meshes
    
    def get_materials(self) -> List[Dict[str, Any]]:
        """Convert Blender material data to standardized format"""
        if not self.blend_data:
            return []
        
        standardized_materials = []
        
        for i, material in enumerate(self.blend_data.get('materials', [])):
            # Convert Blender material to PBR format
            standardized_material = {
                'name': material.get('name', f'Material_{i}'),
                'base_color': material.get('base_color', [0.8, 0.8, 0.8, 1.0]),
                'metallic': material.get('metallic', 0.0),
                'roughness': material.get('roughness', 0.5),
                'emission': material.get('emission', [0.0, 0.0, 0.0]),
                'textures': self._convert_material_textures(material)
            }
            standardized_materials.append(standardized_material)
        
        return standardized_materials
    
    def get_objects(self) -> List[Dict[str, Any]]:
        """Convert Blender object data to standardized format"""
        if not self.blend_data:
            return []
        
        standardized_objects = []
        
        for i, obj in enumerate(self.blend_data.get('objects', [])):
            # Convert Blender object to standardized format
            standardized_object = {
                'name': obj.get('name', f'Object_{i}'),
                'type': obj.get('type', 'MESH'),
                'transform': {
                    'location': obj.get('location', [0.0, 0.0, 0.0]),
                    'rotation': self._convert_rotation(obj.get('rotation', [0.0, 0.0, 0.0])),
                    'scale': obj.get('scale', [1.0, 1.0, 1.0])
                },
                'mesh_index': obj.get('mesh_index'),
                'material_indices': obj.get('material_indices', []),
                'children': obj.get('children', [])
            }
            standardized_objects.append(standardized_object)
        
        return standardized_objects
    
    def get_animations(self) -> List[Dict[str, Any]]:
        """Convert Blender animation data to standardized format"""
        if not self.blend_data:
            return []
        
        # For now, return empty list as animation support is complex
        # TODO: Implement animation conversion
        return []
    
    def get_cameras(self) -> List[Dict[str, Any]]:
        """Convert Blender camera data to standardized format"""
        if not self.blend_data:
            return []
        
        # Extract cameras from objects
        cameras = []
        for obj in self.blend_data.get('objects', []):
            if obj.get('type') == 'CAMERA':
                camera = {
                    'name': obj.get('name', 'Camera'),
                    'type': 'perspective',  # Default to perspective
                    'fov': math.radians(50.0),  # Default FOV
                    'near': 0.1,
                    'far': 1000.0
                }
                cameras.append(camera)
        
        return cameras
    
    def get_lights(self) -> List[Dict[str, Any]]:
        """Convert Blender light data to standardized format"""
        if not self.blend_data:
            return []
        
        # Extract lights from objects
        lights = []
        for obj in self.blend_data.get('objects', []):
            if obj.get('type') in ['LIGHT', 'LAMP']:
                light = {
                    'name': obj.get('name', 'Light'),
                    'type': 'point',  # Default to point light
                    'color': [1.0, 1.0, 1.0],
                    'intensity': 1.0,
                    'range': None
                }
                lights.append(light)
        
    def _convert_coordinates(self, position: List[float]) -> List[float]:
        """
        Convert coordinates from Blender's Z-up system to GLTF's Y-up system.
        
        Args:
            position: [x, y, z] in Blender coordinate system
            
        Returns:
            [x, y, z] in GLTF coordinate system
        """
        # Convert from Blender Z-up to GLTF Y-up
        # Blender: X-right, Y-forward, Z-up
        # GLTF: X-right, Y-up, Z-backward
        x, y, z = position
        return [x, z, -y]
    
    def _convert_vertices(self, vertices: List[Any]) -> List[List[float]]:
        """Convert Blender vertices to standardized format"""
        # Blender uses Z-up, GLTF uses Y-up, so we need to convert
        converted = []
        for vertex in vertices:
            if isinstance(vertex, (list, tuple)) and len(vertex) >= 3:
                # Convert from Blender's Z-up to GLTF's Y-up coordinate system
                x, y, z = vertex[:3]
                converted.append([x, z, -y])  # Blender to GLTF conversion
            else:
                converted.append([0.0, 0.0, 0.0])  # Default vertex
        return converted
    
    def _convert_faces(self, faces: List[Any]) -> List[List[int]]:
        """Convert Blender faces to standardized format"""
        converted = []
        for face in faces:
            if isinstance(face, (list, tuple)):
                # Ensure face has at least 3 vertices (triangle)
                if len(face) >= 3:
                    converted.append(list(face))
        return converted
    
    def _convert_normals(self, normals: List[Any]) -> List[List[float]]:
        """Convert Blender normals to standardized format"""
        converted = []
        for normal in normals:
            if isinstance(normal, (list, tuple)) and len(normal) >= 3:
                # Convert from Blender's Z-up to GLTF's Y-up coordinate system
                x, y, z = normal[:3]
                converted.append([x, z, -y])
            else:
                converted.append([0.0, 1.0, 0.0])  # Default normal (up)
        return converted
    
    def _convert_uvs(self, uvs: List[Any]) -> List[List[float]]:
        """Convert Blender UV coordinates to standardized format"""
        converted = []
        for uv in uvs:
            if isinstance(uv, (list, tuple)) and len(uv) >= 2:
                # Blender UV coordinates are already in the correct format
                converted.append([float(uv[0]), float(uv[1])])
            else:
                converted.append([0.0, 0.0])  # Default UV
        return converted
    
    def _convert_rotation(self, rotation: List[float]) -> List[float]:
        """Convert Blender rotation (Euler) to quaternion"""
        # For now, return Euler angles as-is
        # TODO: Convert to quaternion for proper GLTF format
        if len(rotation) >= 3:
            # Convert from Blender's Z-up to GLTF's Y-up coordinate system
            x, y, z = rotation[:3]
            return [x, z, -y]
        return [0.0, 0.0, 0.0]
    
    def _convert_material_textures(self, material: Dict[str, Any]) -> Dict[str, str]:
        """Convert Blender material textures to standardized format"""
        # For now, return empty dict as texture handling is complex
        # TODO: Implement texture path extraction and conversion
        return {}