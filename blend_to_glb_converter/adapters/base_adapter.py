"""
Base Data Adapter

Defines the interface that all data adapters must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseDataAdapter(ABC):
    """
    Abstract base class for data adapters.
    
    Data adapters are responsible for converting 3D software specific data
    into a standardized format that can be converted to GLTF.
    """
    
    @abstractmethod
    def load_file(self, filepath: str) -> Dict[str, Any]:
        """
        Load and parse a 3D file.
        
        Args:
            filepath: Path to the 3D file
            
        Returns:
            Dictionary containing parsed 3D data
        """
        pass
    
    @abstractmethod
    def get_meshes(self) -> List[Dict[str, Any]]:
        """
        Get mesh data in standardized format.
        
        Returns:
            List of mesh dictionaries with keys:
            - name: str
            - vertices: List[List[float]] (x, y, z coordinates)
            - faces: List[List[int]] (vertex indices)
            - normals: List[List[float]] (normal vectors)
            - uvs: List[List[float]] (texture coordinates)
            - materials: List[int] (material indices per face)
        """
        pass
    
    @abstractmethod
    def get_materials(self) -> List[Dict[str, Any]]:
        """
        Get material data in standardized format.
        
        Returns:
            List of material dictionaries with keys:
            - name: str
            - base_color: List[float] (RGBA)
            - metallic: float
            - roughness: float
            - emission: List[float] (RGB)
            - textures: Dict[str, str] (texture type -> file path)
        """
        pass
    
    @abstractmethod
    def get_objects(self) -> List[Dict[str, Any]]:
        """
        Get object/node data in standardized format.
        
        Returns:
            List of object dictionaries with keys:
            - name: str
            - type: str ('MESH', 'LIGHT', 'CAMERA', etc.)
            - transform: Dict with 'location', 'rotation', 'scale'
            - mesh_index: Optional[int]
            - material_indices: List[int]
            - children: List[int] (indices of child objects)
        """
        pass
    
    @abstractmethod
    def get_animations(self) -> List[Dict[str, Any]]:
        """
        Get animation data in standardized format.
        
        Returns:
            List of animation dictionaries with keys:
            - name: str
            - channels: List[Dict] (animation channels)
            - samplers: List[Dict] (animation samplers)
            - duration: float
        """
        pass
    
    @abstractmethod
    def get_cameras(self) -> List[Dict[str, Any]]:
        """
        Get camera data in standardized format.
        
        Returns:
            List of camera dictionaries with keys:
            - name: str
            - type: str ('perspective' or 'orthographic')
            - fov: Optional[float] (field of view for perspective)
            - near: float
            - far: float
        """
        pass
    
    @abstractmethod
    def get_lights(self) -> List[Dict[str, Any]]:
        """
        Get light data in standardized format.
        
        Returns:
            List of light dictionaries with keys:
            - name: str
            - type: str ('directional', 'point', 'spot')
            - color: List[float] (RGB)
            - intensity: float
            - range: Optional[float]
        """
        pass