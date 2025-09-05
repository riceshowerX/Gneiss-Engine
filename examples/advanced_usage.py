"""
Advanced usage examples for Gneiss-Engine.

This script demonstrates advanced functionality of Gneiss-Engine
with more complex image processing operations and effects.
"""

import os
from pathlib import Path
from typing import Tuple

# Import the Gneiss-Engine Image class
from gneiss import Image


def main():
    """Run advanced examples of Gneiss-Engine functionality."""

    # Create a directory for output files
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Example 1: Advanced image filtering effects
    print("\n=== Example 1: Advanced Filter Effects ===")
    try:
        # Replace with an actual image path
        image_path = "examples/sample_images/sample.jpg"

        if not Path(image_path).exists():
            print(f"Example image not found at {image_path}")
            print("Please place a sample image at this location or update the path.")
            return

        # Load the image
        img = Image(image_path)
        print(f"Loaded image: {img}")

        # Apply multiple filter effects
        processed_img = img.copy()
        processed_img = processed_img.blur(radius=1.5)
        processed_img = processed_img.sharpen(factor=1.8)
        processed_img = processed_img.edge_enhance()
        processed_img = processed_img.adjust_contrast(1.2)

        output_path = output_dir / "example1_advanced_filters.jpg"
        processed_img.save(output_path, quality=95)
        print(f"Saved image with advanced filters: {output_path}")

    except Exception as e:
        print(f"Error in Example 1: {e}")

    # Example 2: Artistic effects
    print("\n=== Example 2: Artistic Effects ===")
    try:
        img = Image(image_path)

        # Create artistic effects
        artistic_img = img.copy()
        artistic_img = artistic_img.emboss()
        artistic_img = artistic_img.posterize(bits=3)
        artistic_img = artistic_img.adjust_saturation(1.5)
        artistic_img = artistic_img.solarize(threshold=192)

        output_path = output_dir / "example2_artistic_effects.jpg"
        artistic_img.save(output_path, quality=90)
        print(f"Saved artistic image: {output_path}")

    except Exception as e:
        print(f"Error in Example 2: {e}")

    # Example 3: Edge detection and enhancement
    print("\n=== Example 3: Edge Detection ===")
    try:
        img = Image(image_path)

        # Edge detection pipeline
        edge_img = img.copy()
        edge_img = edge_img.grayscale()
        edge_img = edge_img.find_edges()
        edge_img = edge_img.adjust_contrast(2.0)
        edge_img = edge_img.invert()

        output_path = output_dir / "example3_edge_detection.jpg"
        edge_img.save(output_path, quality=100)
        print(f"Saved edge detection image: {output_path}")

    except Exception as e:
        print(f"Error in Example 3: {e}")

    # Example 4: Complex chaining with error handling
    print("\n=== Example 4: Complex Operation Chaining ===")
    try:
        img = Image(image_path)

        # Complex processing chain
        final_img = img.copy()
        final_img = final_img.resize(width=1200)
        final_img = final_img.auto_contrast(cutoff=2.0)
        final_img = final_img.equalize()
        final_img = final_img.adjust_brightness(1.1)
        final_img = final_img.adjust_saturation(1.3)
        final_img = final_img.sharpen(factor=1.5)
        final_img = final_img.add_text_watermark(
            text="© Gneiss-Engine Pro",
            position="bottom_right",
            font_size=20,
            color=(255, 255, 255, 200),
            outline_color=(0, 0, 0, 180),
            outline_width=2,
        )
        final_img = final_img.blur(radius=0.5)  # Subtle overall blur

        output_path = output_dir / "example4_complex_processing.webp"
        final_img.to_format("WEBP", quality=85).save(output_path)
        print(f"Saved complex processed image: {output_path}")

    except Exception as e:
        print(f"Error in Example 4: {e}")

    # Example 5: Batch processing simulation
    print("\n=== Example 5: Batch Processing Simulation ===")
    try:
        # Simulate processing multiple variations
        variations = [
            ("vintage", lambda img: img.adjust_color(0.8).blur(radius=0.8)),
            ("modern", lambda img: img.sharpen(factor=2.0).adjust_saturation(1.4)),
            ("bw_art", lambda img: img.grayscale().posterize(bits=2).find_edges()),
            ("warm", lambda img: img.adjust_color(1.2).adjust_brightness(1.1)),
            ("cool", lambda img: img.adjust_color(0.8).blur(radius=0.8)),
        ]

        for style_name, processor in variations:
            try:
                img = Image(image_path)
                processed = processor(img.copy())
                output_path = output_dir / f"example5_{style_name}_style.jpg"
                processed.save(output_path, quality=92)
                print(f"Saved {style_name} style: {output_path}")
            except Exception as e:
                print(f"Error processing {style_name} style: {e}")

    except Exception as e:
        print(f"Error in Example 5: {e}")

    print("\nAdvanced examples completed. Check the 'output' directory for results.")
    print(
        "Note: Some examples may require specific image characteristics to show optimal results."
    )


if __name__ == "__main__":
    main()
