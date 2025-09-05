"""
Basic usage examples for Gneiss-Engine.

This script demonstrates the core functionality of Gneiss-Engine
with simple, easy-to-understand examples.
"""

import os
from pathlib import Path

# Import the Gneiss-Engine Image class
from gneiss import Image

def main():
    """Run basic examples of Gneiss-Engine functionality."""
    
    # Create a directory for output files
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Example 1: Basic image loading and saving
    print("\n=== Example 1: Basic image loading and saving ===")
    try:
        # Replace with an actual image path
        image_path = "examples/sample_images/sample.jpg"
        
        # Check if the example image exists
        if not Path(image_path).exists():
            print(f"Example image not found at {image_path}")
            print("Please place a sample image at this location or update the path.")
            return
        
        # Load the image
        img = Image(image_path)
        print(f"Loaded image: {img}")
        
        # Save the image in a different format
        output_path = output_dir / "example1_output.png"
        img.to_format("PNG").save(output_path)
        print(f"Saved image as PNG: {output_path}")
        
    except Exception as e:
        print(f"Error in Example 1: {e}")
    
    # Example 2: Resizing an image
    print("\n=== Example 2: Resizing an image ===")
    try:
        # Load the image
        img = Image(image_path)
        
        # Resize the image to 50% of its original size
        original_width, original_height = img.image.size
        new_width = original_width // 2
        
        resized_img = img.resize(width=new_width)
        output_path = output_dir / "example2_resized.jpg"
        resized_img.save(output_path)
        
        print(f"Original size: {original_width}x{original_height}")
        print(f"Resized to: {new_width}x{resized_img.image.size[1]}")
        print(f"Saved resized image: {output_path}")
        
    except Exception as e:
        print(f"Error in Example 2: {e}")
    
    # Example 3: Adding a text watermark
    print("\n=== Example 3: Adding a text watermark ===")
    try:
        # Load the image
        img = Image(image_path)
        
        # Add a text watermark
        watermarked_img = img.add_text_watermark(
            text="© Gneiss-Engine",
            position="bottom_right",
            font_size=24,
            color=(255, 255, 255, 180)  # White with 70% opacity
        )
        
        output_path = output_dir / "example3_watermarked.jpg"
        watermarked_img.save(output_path)
        print(f"Saved watermarked image: {output_path}")
        
    except Exception as e:
        print(f"Error in Example 3: {e}")
    
    # Example 4: Chaining multiple operations
    print("\n=== Example 4: Chaining multiple operations ===")
    try:
        # Load the image
        img = Image(image_path)
        
        # Chain multiple operations
        processed_img = img.resize(width=800) \
                          .adjust_brightness(1.2) \
                          .adjust_contrast(1.1) \
                          .sharpen(factor=1.3) \
                          .add_text_watermark(
                              text="© Gneiss-Engine",
                              position="bottom_right",
                              font_size=18,
                              color=(255, 255, 255, 180),
                              outline_color=(0, 0, 0, 120),
                              outline_width=1
                          )
        
        output_path = output_dir / "example4_chained.webp"
        processed_img.to_format("WEBP", quality=90).save(output_path)
        print(f"Saved processed image with chained operations: {output_path}")
        
    except Exception as e:
        print(f"Error in Example 4: {e}")
    
    print("\nExamples completed. Check the 'output' directory for results.")


if __name__ == "__main__":
    main()