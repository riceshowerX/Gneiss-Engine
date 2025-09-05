"""
File operations examples for Gneiss-Engine.

This script demonstrates how to use the file utility functions
for batch renaming and file management.
"""

import os
from pathlib import Path
from glob import glob

# Import Gneiss-Engine utilities
from gneiss.utils.file_utils import (
    get_files_by_extension,
    batch_rename,
    apply_rename,
    generate_sequential_names
)


def main():
    """Run file operations examples."""
    
    # Create a directory for output files
    output_dir = Path("output/file_ops")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Path to sample images directory
    sample_dir = Path("examples/sample_images")
    
    # Check if the sample directory exists
    if not sample_dir.exists():
        print(f"Sample images directory not found at {sample_dir}")
        print("Please create this directory and add some sample images.")
        return
    
    # Example 1: Find all image files in a directory
    print("\n=== Example 1: Find all image files in a directory ===")
    try:
        image_files = get_files_by_extension(
            sample_dir,
            extensions=['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            recursive=True
        )
        
        print(f"Found {len(image_files)} image files:")
        for i, file in enumerate(image_files[:5], 1):  # Show first 5 files
            print(f"  {i}. {file.name}")
        
        if len(image_files) > 5:
            print(f"  ... and {len(image_files) - 5} more")
        
    except Exception as e:
        print(f"Error finding image files: {e}")
    
    # Example 2: Generate sequential names
    print("\n=== Example 2: Generate sequential names ===")
    try:
        sequential_names = generate_sequential_names(
            directory=output_dir,
            base_name="photo_",
            extension="jpg",
            start_number=1,
            padding=3
        )
        
        print(f"Generated {len(sequential_names)} sequential names:")
        for i, name in enumerate(sequential_names[:5], 1):  # Show first 5 names
            print(f"  {i}. {name}")
        
        if len(sequential_names) > 5:
            print(f"  ... and {len(sequential_names) - 5} more")
        
    except Exception as e:
        print(f"Error generating sequential names: {e}")
    
    # Example 3: Batch rename (simulation)
    print("\n=== Example 3: Batch rename (simulation) ===")
    try:
        # Copy some sample files to the output directory for renaming
        if image_files:
            # Create a temporary directory for the rename example
            rename_dir = output_dir / "rename_example"
            rename_dir.mkdir(exist_ok=True)
            
            # Import the required modules
            from shutil import copy2
            
            # Copy a few sample files
            sample_files = []
            for i, src_file in enumerate(image_files[:5]):
                dst_file = rename_dir / f"img_{i+1}{src_file.suffix}"
                copy2(src_file, dst_file)
                sample_files.append(dst_file)
            
            print(f"Copied {len(sample_files)} sample files to {rename_dir}")
            
            # Generate a rename map
            rename_map = batch_rename(
                files=sample_files,
                pattern="img_",
                replacement="photo_",
                use_regex=False
            )
            
            print("Rename map (original -> new):")
            for original, new in rename_map.items():
                print(f"  {Path(original).name} -> {Path(new).name}")
            
            # Apply the renaming
            print("\nApplying rename operations...")
            results = apply_rename(rename_map)
            
            success_count = sum(1 for result in results.values() if result)
            print(f"Successfully renamed {success_count} out of {len(sample_files)} files.")
            
        else:
            print("No sample files available for the rename example.")
        
    except Exception as e:
        print(f"Error in batch rename: {e}")
    
    # Example 4: Batch rename with regex
    print("\n=== Example 4: Batch rename with regex ===")
    try:
        # Find the renamed files from Example 3
        renamed_files = list(Path(rename_dir).glob("photo_*"))
        
        if renamed_files:
            # Generate a rename map using regex
            regex_rename_map = batch_rename(
                files=renamed_files,
                pattern=r"photo_(\d+)",  # Match "photo_" followed by digits
                replacement=r"image_\1",  # Replace with "image_" followed by the captured digits
                use_regex=True
            )
            
            print("Regex rename map (original -> new):")
            for original, new in regex_rename_map.items():
                print(f"  {Path(original).name} -> {Path(new).name}")
            
            # Apply the renaming
            print("\nApplying regex rename operations...")
            results = apply_rename(regex_rename_map)
            
            success_count = sum(1 for result in results.values() if result)
            print(f"Successfully renamed {success_count} out of {len(renamed_files)} files.")
            
        else:
            print("No renamed files available for the regex rename example.")
        
    except Exception as e:
        print(f"Error in regex batch rename: {e}")
    
    print("\nFile operations examples completed. Check the 'output/file_ops' directory for results.")


if __name__ == "__main__":
    main()