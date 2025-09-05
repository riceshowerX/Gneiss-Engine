"""
Create sample images for Gneiss-Engine examples.

This script creates some simple sample images that can be used
with the Gneiss-Engine examples.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def create_sample_image(path, width, height, color, text=None):
    """Create a sample image with optional text."""
    # Create a new image
    img = Image.new('RGB', (width, height), color)
    
    # Add text if provided
    if text:
        draw = ImageDraw.Draw(img)
        
        # Try to use a font that's likely to be available
        try:
            # Try to use Arial, which is common on Windows
            font = ImageFont.truetype("arial.ttf", size=36)
        except IOError:
            # Fall back to default font
            font = ImageFont.load_default()
        
        # Calculate text position to center it
        # In newer Pillow versions, use getbbox() instead of getsize() or textsize()
        try:
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # Fall back for older Pillow versions
            try:
                text_width, text_height = draw.textsize(text, font=font)
            except AttributeError:
                # Very old Pillow versions
                text_width, text_height = font.getsize(text) if hasattr(font, 'getsize') else (width//2, height//2)
        
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Draw the text
        draw.text(position, text, fill=(255, 255, 255), font=font)
    
    # Save the image
    img.save(path)
    print(f"Created sample image: {path}")


def main():
    """Create sample images."""
    # Create the sample images directory
    sample_dir = Path("examples/sample_images")
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Create some sample images with different colors and sizes
    create_sample_image(sample_dir / "sample1.jpg", 800, 600, (255, 0, 0), "Sample 1")
    create_sample_image(sample_dir / "sample2.jpg", 600, 800, (0, 255, 0), "Sample 2")
    create_sample_image(sample_dir / "sample3.jpg", 800, 800, (0, 0, 255), "Sample 3")
    create_sample_image(sample_dir / "sample4.png", 1024, 768, (255, 255, 0), "Sample 4")
    create_sample_image(sample_dir / "sample5.png", 768, 1024, (255, 0, 255), "Sample 5")
    
    print(f"Created {5} sample images in {sample_dir}")


if __name__ == "__main__":
    main()