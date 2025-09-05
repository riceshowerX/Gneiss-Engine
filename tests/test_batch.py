"""
Unit tests for the BatchProcessor class.
"""

import unittest
from pathlib import Path

from PIL import Image as PILImage


from gneiss.core.batch import BatchProcessor


class TestBatchProcessor(unittest.TestCase):
    """Test cases for the BatchProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a test directory
        self.test_dir = Path("tests/test_output")
        self.test_dir.mkdir(parents=True, exist_ok=True)

        # Create a directory for input test images
        self.input_dir = self.test_dir / "input"
        self.input_dir.mkdir(exist_ok=True)

        # Create a directory for output test images
        self.output_dir = self.test_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

        # Create some test images
        self.test_images = []
        for i in range(5):
            path = self.input_dir / f"test_image_{i}.png"
            self._create_test_image(path, width=100, height=100, color=(255, i * 50, 0))
            self.test_images.append(path)

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test files
        for file in self.test_dir.glob("**/*"):
            if file.is_file():
                try:
                    file.unlink()
                except Exception:
                    pass

    def _create_test_image(self, path, width=100, height=100, color=(255, 0, 0)):
        """Create a simple test image."""
        img = PILImage.new("RGB", (width, height), color)
        img.save(path)

    def test_init(self):
        """Test initializing a BatchProcessor."""
        processor = BatchProcessor()
        self.assertIsNotNone(processor)

        processor_with_workers = BatchProcessor(max_workers=2)
        self.assertEqual(processor_with_workers.max_workers, 2)

    def test_process_images(self):
        """Test processing multiple images."""
        processor = BatchProcessor()

        # Define a simple operation
        def resize_operation(img):
            return img.resize(width=50)

        # Process the test images
        results = processor.process_images(
            image_paths=self.test_images,
            operation=resize_operation,
            output_dir=self.output_dir,
            output_suffix="_resized",
            show_progress=False,
        )

        # Check that all operations were successful
        self.assertEqual(len(results), len(self.test_images))
        for input_path, output_path in results.items():
            self.assertIsInstance(output_path, str)
            self.assertTrue(Path(output_path).exists())

            # Check that the output image has the expected size
            with PILImage.open(output_path) as img:
                self.assertEqual(img.size, (50, 50))

    def test_convert_format(self):
        """Test converting multiple images to a different format."""
        processor = BatchProcessor()

        # Convert the test images to JPEG
        results = processor.convert_format(
            image_paths=self.test_images,
            output_format="JPEG",
            output_dir=self.output_dir,
            quality=85,
            show_progress=False,
        )

        # Check that all operations were successful
        self.assertEqual(len(results), len(self.test_images))
        for input_path, output_path in results.items():
            self.assertIsInstance(output_path, str)
            self.assertTrue(Path(output_path).exists())

            # Check that the output image has the expected format
            with PILImage.open(output_path) as img:
                self.assertEqual(img.format, "JPEG")

    def test_resize_images(self):
        """Test resizing multiple images."""
        processor = BatchProcessor()

        # Resize the test images
        results = processor.resize_images(
            image_paths=self.test_images,
            width=75,
            height=50,
            maintain_aspect=False,
            output_dir=self.output_dir,
            show_progress=False,
        )

        # Check that all operations were successful
        self.assertEqual(len(results), len(self.test_images))
        for input_path, output_path in results.items():
            self.assertIsInstance(output_path, str)
            self.assertTrue(Path(output_path).exists())

            # Check that the output image has the expected size
            with PILImage.open(output_path) as img:
                self.assertEqual(img.size, (75, 50))

    def test_add_text_watermark_to_images(self):
        """Test adding a text watermark to multiple images."""
        processor = BatchProcessor()

        # Add a text watermark to the test images
        results = processor.add_text_watermark_to_images(
            image_paths=self.test_images,
            text="Test",
            position="center",
            font_size=24,
            color=(255, 255, 255, 128),
            output_dir=self.output_dir,
            show_progress=False,
        )

        # Check that all operations were successful
        self.assertEqual(len(results), len(self.test_images))
        for input_path, output_path in results.items():
            self.assertIsInstance(output_path, str)
            self.assertTrue(Path(output_path).exists())

    def test_error_handling(self):
        """Test error handling in batch processing."""
        processor = BatchProcessor()

        # Create a list with one valid image and one nonexistent image
        invalid_paths = self.test_images[:1] + [Path("nonexistent_image.jpg")]

        # Define a simple operation
        def resize_operation(img):
            return img.resize(width=50)

        # Process the images
        results = processor.process_images(
            image_paths=invalid_paths,
            operation=resize_operation,
            output_dir=self.output_dir,
            show_progress=False,
        )

        # Check that we got results for all input paths
        self.assertEqual(len(results), len(invalid_paths))

        # Check that the valid image was processed successfully
        self.assertIsInstance(results[str(self.test_images[0])], str)
        self.assertTrue(Path(results[str(self.test_images[0])]).exists())

        # Check that the invalid image resulted in an exception
        self.assertIsInstance(results[str(invalid_paths[1])], Exception)


if __name__ == "__main__":
    unittest.main()
