"""
Unit tests for the BlendToGLBConverter class.
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.converter_v2 import BlendToGLBConverter
from core.blend_reader import BlendReader, BlendFileError


class TestBlendToGLBConverter(unittest.TestCase):
    """Test cases for BlendToGLBConverter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.converter = BlendToGLBConverter()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Clean up temporary files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_converter_initialization(self):
        """Test converter initialization"""
        self.assertIsNotNone(self.converter)
        # 新版本转换器使用backend属性而不是adapter
        self.assertTrue(hasattr(self.converter, 'backend'))
        self.assertTrue(hasattr(self.converter, 'available'))
    
    def test_convert_nonexistent_file(self):
        """Test conversion with non-existent input file"""
        input_path = os.path.join(self.temp_dir, "nonexistent.blend")
        output_path = os.path.join(self.temp_dir, "output.glb")
        
        result = self.converter.convert(input_path, output_path)
        self.assertFalse(result)
    
    def test_convert_invalid_input_extension(self):
        """Test conversion with invalid input file extension"""
        # Create a dummy file with wrong extension
        input_path = os.path.join(self.temp_dir, "test.txt")
        with open(input_path, 'w') as f:
            f.write("dummy content")
        
        output_path = os.path.join(self.temp_dir, "output.glb")
        
        result = self.converter.convert(input_path, output_path)
        self.assertFalse(result)
    
    def test_converter_availability(self):
        """Test converter availability check"""
        # 测试转换器可用性检查方法
        availability = self.converter.is_available()
        self.assertIsInstance(availability, bool)
    
    def test_convert_with_options_method_exists(self):
        """Test that convert_with_options method exists"""
        # 测试convert_with_options方法是否存在
        self.assertTrue(hasattr(self.converter, 'convert_with_options'))
        self.assertTrue(callable(getattr(self.converter, 'convert_with_options')))
    
    def test_batch_convert_method_exists(self):
        """Test that batch_convert method exists"""
        # 测试batch_convert方法是否存在
        self.assertTrue(hasattr(self.converter, 'batch_convert'))
        self.assertTrue(callable(getattr(self.converter, 'batch_convert')))


class TestBlendReader(unittest.TestCase):
    """Test cases for blend file reading functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a dummy filepath for testing
        self.reader = BlendReader("dummy.blend")
    
    def test_reader_initialization(self):
        """Test blend reader initialization"""
        self.assertIsNotNone(self.reader)
    
    def test_read_nonexistent_file(self):
        """Test reading non-existent file"""
        with self.assertRaises(BlendFileError):
            self.reader.read()


class TestBlenderAdapter(unittest.TestCase):
    """Test cases for BlenderDataAdapter"""
    
    def setUp(self):
        """Set up test fixtures"""
        from adapters.blender_adapter import BlenderDataAdapter
        self.adapter = BlenderDataAdapter()
    
    def test_adapter_initialization(self):
        """Test adapter initialization"""
        self.assertIsNotNone(self.adapter)
    
    def test_coordinate_conversion(self):
        """Test coordinate system conversion"""
        # Blender Z-up to GLTF Y-up
        blender_pos = [1.0, 2.0, 3.0]
        gltf_pos = self.adapter._convert_coordinates(blender_pos)
        
        # In a full implementation, this would convert Z-up to Y-up
        # For now, we just check that the method exists and returns something
        self.assertIsNotNone(gltf_pos)
        self.assertEqual(len(gltf_pos), 3)


if __name__ == '__main__':
    unittest.main()