"""
GLTF IO Module

Contains GLTF data structures and serialization functionality extracted from Blender.
"""

from .gltf2_io import *
from .gltf2_io_export import save_gltf

__all__ = ['save_gltf']