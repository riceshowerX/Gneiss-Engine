"""
Batch processing examples for Gneiss-Engine.

This script demonstrates how to use the BatchProcessor class
to process multiple images in parallel.
"""

import os
from pathlib import Path
from glob import glob

# Import Gneiss-Engine classes
from gneiss import Image
from gneiss.core.batch import BatchProcessor


def main():
    """Run batch processing examples."""

    # Create a directory for output files
    output_dir = Path("output/batch")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Path to sample images directory
    sample_dir = Path("examples/sample_images")

    # Check if the sample directory exists
    if not sample_dir.exists():
        print(f"Sample images directory not found at {sample_dir}")
        print("Please create this directory and add some sample images.")
        return

    # Get all image files in the sample directory
    image_paths = []
    for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        image_paths.extend(glob(str(sample_dir / f"*{ext}")))

    if not image_paths:
        print(f"No image files found in {sample_dir}")
        print("Please add some sample images to this directory.")
        return

    print(f"Found {len(image_paths)} images in {sample_dir}")

    # Create a BatchProcessor instance
    batch_processor = BatchProcessor()

    # Example 1: Convert all images to WEBP format
    print("\n=== Example 1: Convert all images to WEBP format ===")
    try:
        results = batch_processor.convert_format(
            image_paths=image_paths,
            output_format="WEBP",
            output_dir=output_dir / "webp_converted",
            quality=90,
            show_progress=True,
        )

        success_count = sum(
            1 for result in results.values() if not isinstance(result, Exception)
        )
        print(
            f"Successfully converted {success_count} out of {len(image_paths)} images to WEBP format."
        )

    except Exception as e:
        print(f"Error in batch conversion: {e}")

    # Example 2: Resize all images to a maximum width of 800px
    print("\n=== Example 2: Resize all images ===")
    try:
        results = batch_processor.resize_images(
            image_paths=image_paths,
            width=800,  # Set maximum width to 800px
            maintain_aspect=True,
            output_dir=output_dir / "resized",
            show_progress=True,
        )

        success_count = sum(
            1 for result in results.values() if not isinstance(result, Exception)
        )
        print(f"Successfully resized {success_count} out of {len(image_paths)} images.")

    except Exception as e:
        print(f"Error in batch resizing: {e}")

    # Example 3: Add text watermark to all images
    print("\n=== Example 3: Add text watermark to all images ===")
    try:
        results = batch_processor.add_text_watermark_to_images(
            image_paths=image_paths,
            text="© Gneiss-Engine",
            position="bottom_right",
            font_size=24,
            color=(255, 255, 255, 180),  # White with 70% opacity
            output_dir=output_dir / "watermarked",
            show_progress=True,
        )

        success_count = sum(
            1 for result in results.values() if not isinstance(result, Exception)
        )
        print(
            f"Successfully watermarked {success_count} out of {len(image_paths)} images."
        )

    except Exception as e:
        print(f"Error in batch watermarking: {e}")

    # Example 4: Custom batch processing
    print("\n=== Example 4: Custom batch processing ===")
    try:
        # Define a custom operation that combines multiple effects
        def custom_operation(img):
            return (
                img.resize(width=1200)
                .adjust_brightness(1.1)
                .adjust_contrast(1.2)
                .add_text_watermark(
                    text="© Gneiss-Engine",
                    position="bottom_right",
                    font_size=18,
                    color=(255, 255, 255, 180),
                )
            )

        results = batch_processor.process_images(
            image_paths=image_paths,
            operation=custom_operation,
            output_dir=output_dir / "custom_processed",
            output_format="JPEG",
            output_suffix="_enhanced",
            show_progress=True,
        )

        success_count = sum(
            1 for result in results.values() if not isinstance(result, Exception)
        )
        print(
            f"Successfully processed {success_count} out of {len(image_paths)} images with custom operation."
        )

    except Exception as e:
        print(f"Error in custom batch processing: {e}")

    print(
        "\nBatch processing examples completed. Check the 'output/batch' directory for results."
    )


if __name__ == "__main__":
    main()
