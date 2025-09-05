"""
Unit tests for the Image class.
"""

import os
import unittest
from pathlib import Path

from PIL import Image as PILImage

from gneiss import Image


class TestImage(unittest.TestCase):
    """Test cases for the Image class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a test directory
        self.test_dir = Path("tests/test_output")
        self.test_dir.mkdir(parents=True, exist_ok=True)

        # Create a simple test image
        self.test_image_path = self.test_dir / "test_image.png"
        self._create_test_image(self.test_image_path)

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test files
        for file in self.test_dir.glob("*"):
            try:
                file.unlink()
            except Exception:
                pass

    def _create_test_image(self, path, width=100, height=100, color=(255, 0, 0)):
        """Create a simple test image."""
        img = PILImage.new("RGB", (width, height), color)
        img.save(path)

    def test_init_from_path(self):
        """Test initializing an Image from a file path."""
        img = Image(self.test_image_path)
        self.assertEqual(img.path, str(self.test_image_path))
        self.assertEqual(img.format, "PNG")
        self.assertEqual(img.image.size, (100, 100))

    def test_init_from_pil_image(self):
        """Test initializing an Image from a PIL Image object."""
        pil_img = PILImage.new("RGB", (200, 200), (0, 255, 0))
        img = Image(pil_img)
        self.assertIsNone(img.path)
        self.assertEqual(img.image.size, (200, 200))

    def test_init_invalid_path(self):
        """Test initializing an Image with an invalid path."""
        with self.assertRaises(FileNotFoundError):
            Image("nonexistent_file.jpg")

    def test_resize(self):
        """Test resizing an image."""
        img = Image(self.test_image_path)

        # Test resize with width only
        resized1 = img.resize(width=50)
        self.assertEqual(resized1.image.size, (50, 50))  # Should maintain aspect ratio

        # Test resize with height only
        resized2 = img.resize(height=25)
        self.assertEqual(resized2.image.size, (25, 25))  # Should maintain aspect ratio

        # Test resize with both width and height, maintaining aspect ratio
        resized3 = img.resize(width=80, height=40)
        self.assertEqual(resized3.image.size[0], 40)  # Should use the smaller ratio

        # Test resize without maintaining aspect ratio
        resized4 = img.resize(width=80, height=40, maintain_aspect=False)
        self.assertEqual(resized4.image.size, (80, 40))

    def test_save(self):
        """Test saving an image."""
        img = Image(self.test_image_path)

        # Save with the same format
        output_path = self.test_dir / "saved_image.png"
        img.save(output_path)
        self.assertTrue(output_path.exists())

        # Save with a different format
        output_path2 = self.test_dir / "saved_image.jpg"
        img.to_format("JPEG").save(output_path2)
        self.assertTrue(output_path2.exists())

        # Check that the format was changed
        with PILImage.open(output_path2) as pil_img:
            self.assertEqual(pil_img.format, "JPEG")

    def test_add_text_watermark(self):
        """Test adding a text watermark."""
        img = Image(self.test_image_path)

        # Add a text watermark
        watermarked = img.add_text_watermark(
            text="Test", position="center", font_size=24, color=(255, 255, 255, 128)
        )

        # Save the watermarked image
        output_path = self.test_dir / "watermarked_image.png"
        watermarked.save(output_path)
        self.assertTrue(output_path.exists())

        # We can't easily verify the watermark visually in a unit test,
        # but we can check that the operation completed without errors
        self.assertIsInstance(watermarked, Image)

    def test_chained_operations(self):
        """Test chaining multiple operations."""
        img = Image(self.test_image_path)

        # Chain multiple operations
        processed = (
            img.resize(width=50)
            .adjust_brightness(1.2)
            .adjust_contrast(1.1)
            .to_format("JPEG", quality=85)
        )

        # Save the processed image
        output_path = self.test_dir / "chained_operations.jpg"
        processed.save(output_path)
        self.assertTrue(output_path.exists())

        # Check that the format was changed
        with PILImage.open(output_path) as pil_img:
            self.assertEqual(pil_img.format, "JPEG")
            self.assertEqual(pil_img.size, (50, 50))


if __name__ == "__main__":
    unittest.main()
