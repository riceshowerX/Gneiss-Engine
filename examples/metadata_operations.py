"""
Metadata operations examples for Gneiss-Engine.

This script demonstrates how to use the metadata utility functions
to work with image metadata.
"""

import json
from pathlib import Path

# Import Gneiss-Engine utilities
from gneiss.utils.metadata_utils import (
    copy_metadata,
    extract_exif,
    get_creation_date,
    get_gps_coordinates,
    get_image_metadata,
    strip_all_metadata,
)


def main():
    """Run metadata operations examples."""

    # Create a directory for output files
    output_dir = Path("output/metadata_ops")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Path to sample images directory
    sample_dir = Path("examples/sample_images")

    # Check if the sample directory exists
    if not sample_dir.exists():
        print(f"Sample images directory not found at {sample_dir}")
        print("Please create this directory and add some sample images.")
        return

    # Find a sample image with EXIF data
    sample_images = list(sample_dir.glob("*.jpg")) + list(sample_dir.glob("*.jpeg"))

    if not sample_images:
        print(f"No JPEG images found in {sample_dir}")
        print("Please add some JPEG images to this directory.")
        return

    sample_image = sample_images[0]
    print(f"Using sample image: {sample_image}")

    # Example 1: Extract EXIF data
    print("\n=== Example 1: Extract EXIF data ===")
    try:
        exif_data = extract_exif(sample_image)

        if exif_data:
            print("EXIF data found:")
            # Print a few key EXIF fields if they exist
            important_tags = [
                "Make",
                "Model",
                "DateTime",
                "ExposureTime",
                "FNumber",
                "ISOSpeedRatings",
            ]
            for tag in important_tags:
                if tag in exif_data:
                    print(f"  {tag}: {exif_data[tag]}")

            # Save the full EXIF data to a JSON file
            exif_json_path = output_dir / "exif_data.json"
            with open(exif_json_path, "w") as f:
                # Convert non-serializable types to strings
                serializable_exif = {}
                for k, v in exif_data.items():
                    try:
                        json.dumps({k: v})  # Test if serializable
                        serializable_exif[k] = v
                    except (TypeError, OverflowError):
                        serializable_exif[k] = str(v)

                json.dump(serializable_exif, f, indent=2)

            print(f"Full EXIF data saved to {exif_json_path}")
        else:
            print("No EXIF data found in the sample image.")

    except Exception as e:
        print(f"Error extracting EXIF data: {e}")

    # Example 2: Get comprehensive metadata
    print("\n=== Example 2: Get comprehensive metadata ===")
    try:
        metadata = get_image_metadata(sample_image)

        print("Basic image information:")
        print(f"  Format: {metadata['basic'].get('format')}")
        print(f"  Mode: {metadata['basic'].get('mode')}")
        print(
            f"  Size: {metadata['basic'].get('width')}x{metadata['basic'].get('height')}"
        )

        # Save the metadata to a JSON file
        metadata_json_path = output_dir / "metadata.json"
        with open(metadata_json_path, "w") as f:
            # Convert non-serializable types to strings
            serializable_metadata = {}
            for section, data in metadata.items():
                serializable_metadata[section] = {}
                for k, v in data.items():
                    try:
                        json.dumps({k: v})  # Test if serializable
                        serializable_metadata[section][k] = v
                    except (TypeError, OverflowError):
                        serializable_metadata[section][k] = str(v)

            json.dump(serializable_metadata, f, indent=2)

        print(f"Full metadata saved to {metadata_json_path}")

    except Exception as e:
        print(f"Error getting comprehensive metadata: {e}")

    # Example 3: Get creation date
    print("\n=== Example 3: Get creation date ===")
    try:
        creation_date = get_creation_date(sample_image)

        if creation_date:
            print(f"Image creation date: {creation_date}")
        else:
            print("No creation date found in the image metadata.")

    except Exception as e:
        print(f"Error getting creation date: {e}")

    # Example 4: Get GPS coordinates
    print("\n=== Example 4: Get GPS coordinates ===")
    try:
        gps_coords = get_gps_coordinates(sample_image)

        if gps_coords:
            print("GPS coordinates found:")
            print(f"  Latitude: {gps_coords['latitude']}")
            print(f"  Longitude: {gps_coords['longitude']}")
            print(
                f"  Google Maps link: https://maps.google.com/?q={gps_coords['latitude']},{gps_coords['longitude']}"
            )
        else:
            print("No GPS coordinates found in the image metadata.")

    except Exception as e:
        print(f"Error getting GPS coordinates: {e}")

    # Example 5: Strip metadata
    print("\n=== Example 5: Strip metadata ===")
    try:
        # Copy the sample image to the output directory
        from shutil import copy2

        stripped_image_path = output_dir / f"stripped_{sample_image.name}"
        copy2(sample_image, stripped_image_path)

        # Strip metadata
        success = strip_all_metadata(stripped_image_path)

        if success:
            print(f"Successfully stripped metadata from {stripped_image_path}")

            # Verify that metadata was stripped
            stripped_exif = extract_exif(stripped_image_path)
            if not stripped_exif:
                print(
                    "Verification successful: No EXIF data found in the stripped image."
                )
            else:
                print(
                    "Warning: Some EXIF data may still be present in the stripped image."
                )
        else:
            print(f"Failed to strip metadata from {stripped_image_path}")

    except Exception as e:
        print(f"Error stripping metadata: {e}")

    # Example 6: Copy metadata
    print("\n=== Example 6: Copy metadata ===")
    try:
        # Create a copy of the sample image without metadata
        source_image_path = sample_image
        target_image_path = output_dir / f"target_{sample_image.name}"

        # First create a stripped copy as the target
        from shutil import copy2

        copy2(sample_image, target_image_path)
        strip_all_metadata(target_image_path)

        # Copy metadata from source to target
        success = copy_metadata(source_image_path, target_image_path)

        if success:
            print(
                f"Successfully copied metadata from {source_image_path.name} to {target_image_path.name}"
            )

            # Verify that metadata was copied
            source_exif = extract_exif(source_image_path)
            target_exif = extract_exif(target_image_path)

            if source_exif and target_exif:
                # Check a few key EXIF fields
                important_tags = ["Make", "Model", "DateTime"]
                matches = sum(
                    1
                    for tag in important_tags
                    if tag in source_exif
                    and tag in target_exif
                    and source_exif[tag] == target_exif[tag]
                )

                if matches > 0:
                    print(
                        f"Verification successful: {matches} key EXIF fields match between source and target."
                    )
                else:
                    print(
                        "Warning: No matching EXIF fields found between source and target."
                    )
            else:
                print("Warning: Could not verify metadata copying.")
        else:
            print(
                f"Failed to copy metadata from {source_image_path.name} to {target_image_path.name}"
            )

    except Exception as e:
        print(f"Error copying metadata: {e}")

    print(
        "\nMetadata operations examples completed. Check the 'output/metadata_ops' directory for results."
    )


if __name__ == "__main__":
    main()
