"""
Unit tests for the file utility functions.
"""

import os
import unittest
from pathlib import Path
from typing import List

from gneiss.utils.file_utils import (
    apply_rename,
    batch_rename,
    generate_sequential_names,
    get_files_by_extension,
    find_images,
    ensure_directory_exists,
    get_unique_filename,
    generate_output_filename,
    move_files_with_progress,
    group_files_by_extension,
    get_file_size,
    remove_files_with_progress,
    filter_files_by_pattern
)


class TestFileUtils(unittest.TestCase):
    """Test cases for the file utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a test directory
        self.test_dir = Path("tests/test_output")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.subdir1 = self.test_dir / "subdir1"
        self.subdir1.mkdir(exist_ok=True)
        
        self.subdir2 = self.test_dir / "subdir2"
        self.subdir2.mkdir(exist_ok=True)

        # Create some test files with different extensions
        self.test_files = []
        
        # Root directory files
        for ext in [".jpg", ".png", ".txt", ".pdf"]:
            for i in range(2):
                path = self.test_dir / f"test_file_{i}{ext}"
                path.touch()
                self.test_files.append(path)
        
        # Subdirectory 1 files
        for ext in [".jpg", ".png"]:
            for i in range(2):
                path = self.subdir1 / f"sub1_file_{i}{ext}"
                path.touch()
                self.test_files.append(path)
        
        # Subdirectory 2 files
        for ext in [".gif", ".webp"]:
            for i in range(2):
                path = self.subdir2 / f"sub2_file_{i}{ext}"
                path.touch()
                self.test_files.append(path)
        
        # Create a test file with content for size testing
        self.content_file = self.test_dir / "content_file.txt"
        with open(self.content_file, "w") as f:
            f.write("x" * 1024)  # 1KB of data
        self.test_files.append(self.content_file)

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test files recursively
        def remove_recursively(path):
            if path.is_dir():
                for item in path.iterdir():
                    remove_recursively(item)
                path.rmdir()
            elif path.is_file():
                path.unlink()
        
        # Remove all test files and directories
        if self.test_dir.exists():
            for item in self.test_dir.iterdir():
                remove_recursively(item)

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


    def test_find_images(self):
        """Test finding image files."""
        # Test non-recursive search
        images = find_images(self.test_dir, recursive=False)
        expected_count = 4  # 2 jpg + 2 png in root dir
        self.assertEqual(len(images), expected_count)
        
        # Test recursive search
        images_recursive = find_images(self.test_dir, recursive=True)
        expected_count_recursive = 8  # 2 jpg + 2 png + 2 gif + 2 webp
        self.assertEqual(len(images_recursive), expected_count_recursive)
        
        # Test with specific extensions
        jpg_png_images = find_images(self.test_dir, extensions=[".jpg", ".png"], recursive=True)
        expected_jpg_png = 8  # 2 jpg + 2 png in root + 2 jpg + 2 png in subdir1
        self.assertEqual(len(jpg_png_images), expected_jpg_png)
        
        # Test with non-existent directory
        with self.assertRaises(ValueError):
            find_images("nonexistent_directory")
    
    def test_ensure_directory_exists(self):
        """Test ensuring directory exists."""
        # Test with existing directory
        ensure_directory_exists(self.test_dir)
        self.assertTrue(self.test_dir.exists())
        
        # Test with new directory
        new_dir = self.test_dir / "new_subdir"
        ensure_directory_exists(new_dir)
        self.assertTrue(new_dir.exists())
        
        # Test with nested directories
        nested_dir = self.test_dir / "parent" / "child" / "grandchild"
        ensure_directory_exists(nested_dir)
        self.assertTrue(nested_dir.exists())
    
    def test_get_unique_filename(self):
        """Test getting unique filename."""
        # Test with non-existent file
        unique_name = get_unique_filename(self.test_dir / "new_file.jpg")
        self.assertEqual(unique_name, self.test_dir / "new_file.jpg")
        
        # Test with existing file
        existing_file = self.test_dir / "test_file_0.jpg"  # This exists from setUp
        unique_name2 = get_unique_filename(existing_file)
        self.assertTrue(unique_name2 != existing_file)
        self.assertTrue("(1)" in str(unique_name2))
        
        # Test with multiple existing versions
        for i in range(3):
            test_name = self.test_dir / f"test_unique_{i}.txt"
            test_name.touch()
        
        unique_name3 = get_unique_filename(self.test_dir / "test_unique_0.txt")
        self.assertTrue("(3)" in str(unique_name3))
    
    def test_generate_output_filename(self):
        """Test generating output filename."""
        input_file = self.test_dir / "test_file_0.jpg"
        output_dir = self.test_dir / "output"
        
        # Test with default parameters
        output_path = generate_output_filename(input_file, output_dir=output_dir)
        self.assertEqual(output_path, output_dir / "test_file_0.jpg")
        
        # Test with suffix
        output_path2 = generate_output_filename(input_file, output_dir=output_dir, suffix="_processed")
        self.assertEqual(output_path2, output_dir / "test_file_0_processed.jpg")
        
        # Test with different extension
        output_path3 = generate_output_filename(input_file, output_dir=output_dir, extension=".png")
        self.assertEqual(output_path3, output_dir / "test_file_0.png")
    
    def test_group_files_by_extension(self):
        """Test grouping files by extension."""
        # Get all files
        all_files = [str(f) for f in self.test_files]
        
        # Group by extension
        grouped = group_files_by_extension(all_files)
        
        # Check if all expected extensions are present
        expected_extensions = [".jpg", ".png", ".txt", ".pdf", ".gif", ".webp"]
        for ext in expected_extensions:
            self.assertIn(ext, grouped)
        
        # Check counts
        self.assertEqual(len(grouped[".jpg"]), 4)  # 2 in root + 2 in subdir1
        self.assertEqual(len(grouped[".png"]), 4)  # 2 in root + 2 in subdir1
        self.assertEqual(len(grouped[".txt"]), 3)  # 2 in root + 1 content file
    
    def test_get_file_size(self):
        """Test getting file size."""
        # Test with known file size
        size = get_file_size(self.content_file)
        self.assertEqual(size, 1024)  # We wrote 1KB of data
        
        # Test with human-readable format
        human_size = get_file_size(self.content_file, human_readable=True)
        self.assertTrue(human_size.startswith("1.0"))  # Should be around 1.0 KB
        
        # Test with bytes input
        human_size2 = get_file_size(1048576, human_readable=True)  # 1MB in bytes
        self.assertTrue(human_size2.startswith("1.0"))
    
    def test_filter_files_by_pattern(self):
        """Test filtering files by pattern."""
        # Get all files
        all_files = [str(f) for f in self.test_files]
        
        # Test with simple pattern
        filtered = filter_files_by_pattern(all_files, "test_file")
        self.assertTrue(len(filtered) > 0)
        for file in filtered:
            self.assertIn("test_file", file)
        
        # Test with regex pattern
        filtered_regex = filter_files_by_pattern(all_files, r"^test_file_\d+\.jpg$", use_regex=True)
        self.assertEqual(len(filtered_regex), 2)  # Should match the two jpg files in root dir
    
    def test_move_files_with_progress(self):
        """Test moving files with progress tracking."""
        # Create source and destination directories
        source_dir = self.test_dir / "source"
        dest_dir = self.test_dir / "destination"
        source_dir.mkdir(exist_ok=True)
        ensure_directory_exists(dest_dir)
        
        # Create test files to move
        files_to_move = []
        for i in range(3):
            file_path = source_dir / f"move_test_{i}.txt"
            file_path.touch()
            files_to_move.append(str(file_path))
        
        # Move files
        results = move_files_with_progress(files_to_move, str(dest_dir))
        
        # Check results
        self.assertEqual(len(results), len(files_to_move))
        for original, moved in results.items():
            self.assertTrue(moved)
            self.assertFalse(Path(original).exists())
            self.assertTrue(Path(dest_dir / Path(original).name).exists())
    
    def test_remove_files_with_progress(self):
        """Test removing files with progress tracking."""
        # Create test files to remove
        files_to_remove = []
        for i in range(3):
            file_path = self.test_dir / f"remove_test_{i}.txt"
            file_path.touch()
            files_to_remove.append(str(file_path))
        
        # Remove files
        results = remove_files_with_progress(files_to_remove)
        
        # Check results
        self.assertEqual(len(results), len(files_to_remove))
        for file_path, removed in results.items():
            self.assertTrue(removed)
            self.assertFalse(Path(file_path).exists())


if __name__ == "__main__":
    unittest.main()
