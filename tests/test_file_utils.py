"""
Unit tests for the file utility functions.
"""

import os
import unittest
from pathlib import Path

from gneiss.utils.file_utils import (
    apply_rename,
    batch_rename,
    generate_sequential_names,
    get_files_by_extension,
)


class TestFileUtils(unittest.TestCase):
    """Test cases for the file utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a test directory
        self.test_dir = Path("tests/test_output")
        self.test_dir.mkdir(parents=True, exist_ok=True)

        # Create some test files with different extensions
        self.test_files = []
        for ext in [".jpg", ".png", ".txt", ".pdf"]:
            for i in range(2):
                path = self.test_dir / f"test_file_{i}{ext}"
                path.touch()
                self.test_files.append(path)

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test files
        for file in self.test_dir.glob("*"):
            try:
                file.unlink()
            except Exception:
                pass

    def test_get_files_by_extension(self):
        """Test getting files by extension."""
        # Get all image files
        image_files = get_files_by_extension(
            self.test_dir, extensions=[".jpg", ".png"], recursive=False
        )

        # Check that we got the expected number of files
        self.assertEqual(len(image_files), 4)  # 2 JPG + 2 PNG

        # Check that all files have the expected extensions
        for file in image_files:
            self.assertIn(file.suffix.lower(), [".jpg", ".png"])

        # Get only JPG files
        jpg_files = get_files_by_extension(
            self.test_dir, extensions=[".jpg"], recursive=False
        )

        # Check that we got the expected number of files
        self.assertEqual(len(jpg_files), 2)  # 2 JPG

        # Check that all files have the expected extension
        for file in jpg_files:
            self.assertEqual(file.suffix.lower(), ".jpg")

    def test_get_files_by_extension_nonexistent_dir(self):
        """Test getting files from a nonexistent directory."""
        with self.assertRaises(FileNotFoundError):
            get_files_by_extension(
                "nonexistent_directory", extensions=[".jpg"], recursive=False
            )

    def test_batch_rename(self):
        """Test batch renaming files."""
        # Get all test files
        files = [str(file) for file in self.test_files]

        # Generate a rename map
        rename_map = batch_rename(
            files=files,
            pattern="test_file",
            replacement="renamed_file",
            use_regex=False,
        )

        # Check that we got a rename map for all files
        self.assertEqual(len(rename_map), len(files))

        # Check that the rename map has the expected replacements
        for original, new in rename_map.items():
            self.assertIn("test_file", original)
            self.assertIn("renamed_file", new)
            self.assertNotIn("test_file", new)

    def test_batch_rename_with_regex(self):
        """Test batch renaming files with regex."""
        # Get all test files
        files = [str(file) for file in self.test_files]

        # Generate a rename map with regex
        rename_map = batch_rename(
            files=files,
            pattern=r"test_file_(\d+)",
            replacement=r"file_\1_renamed",
            use_regex=True,
        )

        # Check that we got a rename map for all files
        self.assertEqual(len(rename_map), len(files))

        # Check that the rename map has the expected replacements
        for original, new in rename_map.items():
            self.assertIn("test_file_", original)
            self.assertIn("file_", new)
            self.assertIn("_renamed", new)
            self.assertNotIn("test_file_", new)

    def test_apply_rename(self):
        """Test applying a rename map."""
        # Create some specific test files for renaming
        rename_test_dir = self.test_dir / "rename_test"
        rename_test_dir.mkdir(exist_ok=True)

        test_files = []
        for i in range(3):
            path = rename_test_dir / f"test_file_{i}.txt"
            path.touch()
            test_files.append(path)

        # Generate a rename map
        rename_map = {}
        for file in test_files:
            new_name = file.parent / f"renamed_{file.name}"
            rename_map[str(file)] = str(new_name)

        # Apply the rename map
        results = apply_rename(rename_map)

        # Check that all renames were successful
        self.assertEqual(len(results), len(test_files))
        for original, success in results.items():
            self.assertTrue(success)

        # Check that the files were actually renamed
        for original, new in rename_map.items():
            self.assertFalse(Path(original).exists())
            self.assertTrue(Path(new).exists())

    def test_apply_rename_conflict(self):
        """Test applying a rename map with conflicts."""
        # Create some specific test files for renaming
        conflict_test_dir = self.test_dir / "conflict_test"
        conflict_test_dir.mkdir(exist_ok=True)

        # Create two files: one to be renamed and one that will cause a conflict
        source_file = conflict_test_dir / "source.txt"
        target_file = conflict_test_dir / "target.txt"

        source_file.touch()
        target_file.touch()

        # Generate a rename map with a conflict
        rename_map = {str(source_file): str(target_file)}  # This will cause a conflict

        # Apply the rename map
        results = apply_rename(rename_map)

        # Check that the rename failed due to the conflict
        self.assertEqual(len(results), 1)
        self.assertFalse(results[str(source_file)])

        # Check that both files still exist
        self.assertTrue(source_file.exists())
        self.assertTrue(target_file.exists())

    def test_generate_sequential_names(self):
        """Test generating sequential filenames."""
        # Count the number of files in the test directory
        file_count = len([f for f in self.test_dir.iterdir() if f.is_file()])

        # Generate sequential names
        names = generate_sequential_names(
            directory=self.test_dir,
            base_name="seq_",
            extension="jpg",
            start_number=1,
            padding=3,
        )

        # Check that we got the expected number of names
        # (should match the number of files in the test directory)
        self.assertEqual(len(names), file_count)

        # Check that the names have the expected format
        for i, name in enumerate(names, 1):
            self.assertTrue(name.startswith("seq_"))
            self.assertTrue(name.endswith(".jpg"))
            self.assertIn(f"{i:03d}", name)

    def test_generate_sequential_names_nonexistent_dir(self):
        """Test generating sequential names for a nonexistent directory."""
        with self.assertRaises(FileNotFoundError):
            generate_sequential_names(
                directory="nonexistent_directory",
                base_name="seq_",
                extension="jpg",
                start_number=1,
                padding=3,
            )


if __name__ == "__main__":
    unittest.main()
