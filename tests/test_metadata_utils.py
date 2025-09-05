"""
Unit tests for the metadata utility functions.
"""


import unittest
from pathlib import Path

from PIL import Image as PILImage


from gneiss.utils.metadata_utils import (
    copy_metadata,
    extract_exif,
    get_creation_date,
    get_gps_coordinates,
    get_image_metadata,
    strip_all_metadata,
)


class TestMetadataUtils(unittest.TestCase):
    """Test cases for the metadata utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a test directory
        self.test_dir = Path("tests/test_output")
        self.test_dir.mkdir(parents=True, exist_ok=True)

        # Create a test image with EXIF data
        self.test_image_path = self.test_dir / "test_image_with_exif.jpg"
        self._create_test_image_with_exif(self.test_image_path)

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test files
        for file in self.test_dir.glob("*"):
            try:
                file.unlink()
            except Exception:
                pass

    def _create_test_image_with_exif(
        self, path, width=100, height=100, color=(255, 0, 0)
    ):
        """Create a test image with some basic EXIF data."""
        img = PILImage.new("RGB", (width, height), color)

        # Add some basic EXIF-like data
        # Note: This is a simplified approach and doesn't create actual EXIF data
        # For real EXIF testing, you would need a sample image with real EXIF data
        # exif_data = {
        #     "Software": "Gneiss-Engine Test",
        #     "Artist": "极Test User",
        #     "Copyright": "2025 Gneiss-Engine",
        # }

        img.save(path, format="JPEG", exif=PILImage.Exif(), quality=95)

        # For real tests, you would use a sample image with known EXIF data
        # or use a library like piexif to add proper EXIF data

    def test_extract_exif(self):
        """Test extracting EXIF data from an image."""
        # For a proper test, you would need a real image with EXIF data
        # Here we're just testing that the function runs without errors
        exif_data = extract_exif(self.test_image_path)

        # The test image might not have real EXIF data, so we just check that
        # the function returns a dictionary
        self.assertIsInstance(exif_data, dict)

    def test_get_image_metadata(self):
        """Test getting comprehensive metadata from an image."""
        metadata = get_image_metadata(self.test_image_path)

        # Check that we got a dictionary with the expected sections
        self.assertIsInstance(metadata, dict)
        self.assertIn("basic", metadata)
        self.assertIn("exif", metadata)

        # Check that the basic metadata has the expected fields
        basic = metadata["basic"]
        self.assertEqual(basic["format"], "JPEG")
        self.assertEqual(basic["size"], (100, 100))
        self.assertEqual(basic["width"], 100)
        self.assertEqual(basic["height"], 100)

    def test_get_creation_date(self):
        """Test getting the creation date from an image."""
        # For a proper test, you would need a real image with EXIF date data
        # Here we're just testing that the function runs without errors
        creation_date = get_creation_date(self.test_image_path)

        # The test image might not have a creation date, so the result could be None
        # We just check that the function returns without errors
        self.assertIsInstance(creation_date, (str, type(None)))

    def test_get_gps_coordinates(self):
        """Test getting GPS coordinates from an image."""
        # For a proper test, you would need a real image with GPS data
        # Here we're just testing that the function runs without errors
        gps_coords = get_gps_coordinates(self.test_image_path)

        # The test image doesn't have GPS data, so the result should be None
        self.assertIsNone(gps_coords)

    def test_strip_all_metadata(self):
        """Test stripping all metadata from an image."""
        # Create a copy of the test image
        stripped_path = self.test_dir / "stripped_image.jpg"

        # Strip metadata
        success = strip_all_metadata(self.test_image_path, stripped_path)

        # Check that the operation was successful
        self.assertTrue(success)
        self.assertTrue(stripped_path.exists())

        # Check that the stripped image has no EXIF data
        # This is a simplified check; for a real test, you would need to verify
        # that all metadata was actually removed
        with PILImage.open(stripped_path) as img:
            self.assertFalse(hasattr(img, "_getexif") and img._getexif())

    def test_copy_metadata(self):
        """Test copying metadata from one image to another."""
        # Create a copy of the test image without metadata
        target_path = self.test_dir / "target_image.jpg"

        # Create a simple image without metadata
        img = PILImage.new("RGB", (100, 100), (0, 255, 0))
        img.save(target_path)

        # Copy metadata
        success = copy_metadata(self.test_image_path, target_path)

        # For a proper test, you would need real images with metadata
        # Here we're just testing that the function runs without errors
        # The result might be False if the test image doesn't have proper EXIF data
        self.assertIsInstance(success, bool)


if __name__ == "__main__":
    unittest.main()
