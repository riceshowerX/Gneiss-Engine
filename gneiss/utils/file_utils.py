"""
File utility functions for Gneiss-Engine.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Union


def get_files_by_extension(
    directory: Union[str, Path], extensions: List[str], recursive: bool = True
) -> List[Path]:
    """
    Get all files with the specified extensions in the directory.

    Args:
        directory: The directory to search in.
        extensions: List of file extensions to include (e.g., ['.jpg', '.png']).
        recursive: Whether to search recursively in subdirectories.

    Returns:
        A list of Path objects for the matching files.
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Normalize extensions to lowercase with leading dot
    normalized_extensions = [
        ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions
    ]

    result = []

    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in normalized_extensions:
                    result.append(file_path)
    else:
        for file in directory.iterdir():
            if file.is_file() and file.suffix.lower() in normalized_extensions:
                result.append(file)

    return result


def batch_rename(
    files: List[Union[str, Path]],
    pattern: str,
    replacement: str,
    use_regex: bool = False,
) -> Dict[str, str]:
    """
    Rename multiple files based on a pattern.

    Args:
        files: List of file paths to rename.
        pattern: The pattern to search for in the filename.
        replacement: The replacement string.
        use_regex: Whether to use regex for pattern matching.

    Returns:
        A dictionary mapping original filenames to new filenames.

    Example:
        >>> files = ['img001.jpg', 'img002.jpg']
        >>> batch_rename(files, 'img', 'photo')
        {'img001.jpg': 'photo001.jpg', 'img002.jpg': 'photo002.jpg'}
    """
    result = {}

    for file_path in files:
        file_path = Path(file_path)
        original_name = file_path.name
        parent_dir = file_path.parent

        if use_regex:
            new_name = re.sub(pattern, replacement, original_name)
        else:
            new_name = original_name.replace(pattern, replacement)

        new_path = parent_dir / new_name

        # Store the mapping without actually renaming
        result[str(file_path)] = str(new_path)

    return result


def apply_rename(rename_map: Dict[str, str]) -> Dict[str, bool]:
    """
    Apply the renaming based on a rename map.

    Args:
        rename_map: A dictionary mapping original filenames to new filenames.

    Returns:
        A dictionary indicating success/failure for each file.
    """
    result = {}

    for original, new in rename_map.items():
        original_path = Path(original)
        new_path = Path(new)

        try:
            # Check if the destination already exists
            if new_path.exists():
                result[original] = False
                continue

            # Rename the file
            original_path.rename(new_path)
            result[original] = True
        except Exception:
            result[original] = False

    return result


def generate_sequential_names(
    directory: Union[str, Path],
    base_name: str,
    extension: str,
    start_number: int = 1,
    padding: int = 3,
) -> List[str]:
    """
    Generate sequential filenames for a directory.

    Args:
        directory: The directory to generate names for.
        base_name: The base name for the files.
        extension: The file extension.
        start_number: The starting number for the sequence.
        padding: The number of digits to pad the sequence number with.

    Returns:
        A list of generated filenames.

    Example:
        >>> generate_sequential_names('.', 'img', 'jpg', 1, 3)
        ['img001.jpg', 'img002.jpg', ...]
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Normalize extension
    if not extension.startswith("."):
        extension = f".{extension}"

    # Get existing files to determine how many files to generate
    existing_files = list(directory.iterdir())
    file_count = len([f for f in existing_files if f.is_file()])

    # Generate sequential names
    result = []
    for i in range(start_number, start_number + file_count):
        filename = f"{base_name}{str(i).zfill(padding)}{extension}"
        result.append(filename)

    return result
