# Gneiss-Engine 🪨

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![PyPI Version](https://img.shields.io/badge/pypi-v0.0.1_alpha-orange)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

*A rock-solid, high-performance Python core for metamorphic image manipulation.*

---

## About The Project

In software development, handling fundamental image tasks like batch conversion, intelligent renaming, or optimization can often feel fragmented and require multiple libraries. **Gneiss-Engine** is being built to solve this by providing a single, powerful, and reliable core for all common image processing needs.

The name "Gneiss" (pronounced /naɪs/, like "nice") is inspired by the metamorphic rock, which is formed when existing rocks are fundamentally transformed under immense heat and pressure. In the same spirit, Gneiss-Engine is designed as a foundational toolkit that **re-forms and restructures** your image assets, providing a solid, layered foundation for all manipulation tasks.

## ✨ Core Features (Current Implementation)

Gneiss-Engine has implemented the following key capabilities:

*   **🔄 Metamorphic Conversion:** A simple and powerful API for converting images between various formats (e.g., `PNG`, `JPEG`, `WEBP`, `AVIF`), with advanced format detection.
*   **⚡ Batch Processing:** Efficient parallel processing of multiple images with progress tracking and error handling.
*   **🔍 High-Quality Resizing:** Easy-to-use functions for scaling images while maintaining aspect ratio and image quality using advanced resampling techniques.
*   **🔄 Transformations:** Comprehensive support for rotations, cropping, flipping, and perspective transformations.
*   **💧 Watermarking:** A fluent interface to add text or image-based watermarks with control over opacity and position.
*   **🛠️ Metadata Management:** Complete tools for reading, writing, and stripping image metadata (EXIF, IPTC, etc.).
*   **🔧 File Operations:** Advanced utilities for finding, filtering, renaming, and managing image files in bulk.
*   **⚡ Performance-Focused:** Built with resource awareness and optimized for multi-threaded processing.

## 🚀 Our Philosophy

1.  **Simplicity First:** We believe powerful tools don't have to be complicated. Gneiss-Engine features a clean, chainable, and highly readable API.
2.  **Extensibility:** Designed as a core "engine," it is easy to extend with custom plugins and functionality.
3.  **Reliability:** A strong focus on comprehensive testing and predictable behavior. It should be the bedrock of your image processing pipeline.

## Installation

```bash
# Basic installation
pip install gneiss-engine

# Installation with all optional dependencies
pip install gneiss-engine[all]

# Installation with specific format support
# AVIF format support
pip install gneiss-engine[avif]

# HEIC format support
pip install gneiss-engine[heic]
```

## Quick Start

### Basic Image Processing

```python
from gneiss.core import Image

# Open an image
img = Image.open('example.jpg')

# Resize and save
img.resize(width=800, height=600, maintain_aspect=True).save('resized.jpg')

# Apply multiple operations and save in a different format
img.rotate(90)
   .crop(left=10, top=10, right=500, bottom=500)
   .convert_to_grayscale()
   .save('processed.png')

# Create a thumbnail
img.thumbnail(size=(128, 128), resample='LANCZOS')
img.save('thumbnail.jpg')
```

### Batch Processing

```python
from gneiss.core import BatchProcessor
import os

# Create processor
processor = BatchProcessor(max_workers=4)

# Get all images in a directory
image_dir = 'images/'
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) 
               if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Batch convert format
results = processor.convert_format(
    image_paths=image_paths,
    output_format='webp',
    output_dir='converted/',
    quality=80,
    show_progress=True,
    skip_existing=True
)

# Print processing results
print(f"Processing summary:")
print(f"Total files: {results['metadata']['total']}")
print(f"Success: {results['metadata']['success']}")
print(f"Failed: {results['metadata']['failed']}")
print(f"Skipped: {results['metadata']['skipped']}")
```

## Example Scripts

Gneiss-Engine provides a collection of example scripts to demonstrate the library's capabilities:

1. **Create Sample Images** - Generate test images for processing
   ```bash
   python examples/create_sample_images.py
   ```

2. **File Operations** - Demonstrate file management and batch operations
   ```bash
   python examples/file_operations.py
   ```

3. **Batch Processing** - Showcase various batch image processing operations
   ```bash
   python examples/batch_processing.py
   ```

4. **Advanced Image Processing** - Demonstrate advanced techniques including enhancement, edge detection, and segmentation
   ```bash
   python examples/advanced_image_processing.py
   ```

5. **Example Documentation** - Learn more about all example scripts
   ```bash
   cat examples/README.md
   ```

## Project Structure

```
Gneiss-Engine/
├── gneiss/             # Core package
│   ├── core/           # Main functionality (Image, BatchProcessor)
│   └── utils/          # Utility functions (file operations, metadata)
├── examples/           # Example scripts
├── tests/              # Unit tests
├── docs/               # Documentation
├── setup.py            # Package setup
└── README.md           # Project documentation
```

## How to Contribute

We welcome contributions to improve Gneiss-Engine! If you have a suggestion, find a bug, or want to contribute code:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For more details, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

Distributed under the MIT License. See `LICENSE` file for more information.
