# Gneiss-Engine 🪨

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yourusername/gneiss-engine)
[![PyPI Version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/gneiss-engine/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A rock-solid, high-performance Python core for metamorphic image manipulation.

## About The Project

In software development, handling fundamental image tasks like batch conversion, intelligent renaming, or optimization can often feel fragmented and require multiple libraries. Gneiss-Engine is being built to solve this by providing a single, powerful, and reliable core for all common image processing needs.

The name "Gneiss" (pronounced /naɪs/, like "nice") is inspired by the metamorphic rock, which is formed when existing rocks are fundamentally transformed under immense heat and pressure. In the same spirit, Gneiss-Engine is designed as a foundational toolkit that re-forms and restructures your image assets, providing a solid, layered foundation for all manipulation tasks.

## ⚠️ Important Note: Personal Developer's Experimental Project

Gneiss-Engine is currently an **experimental project** developed by a **single individual** in their spare time, at a **very early stage of development**. This means:

1. This is a **personal project** with no company or team backing
2. Development progress **depends entirely on personal availability** and may be very slow
3. Core features and APIs **may change significantly at any time**
4. **Not recommended** for production use in its current state
5. The project **may remain experimental indefinitely** with no guarantee of ongoing maintenance

While I'll do my best to improve this project, please understand that as a solo developer, both time and resources are limited. Your understanding and patience are greatly appreciated!

We welcome ideas, feedback, and future contributors to help shape its direction.

## ✨ Core Features (Vision)

Gneiss-Engine is being designed with the following key capabilities in mind:

- 🔄 **Metamorphic Conversion**: A simple and powerful API for converting images between various formats (e.g., PNG, JPEG, WEBP, AVIF), akin to a rock changing its fundamental structure.
- ✍️ **Intelligent Renaming**: Advanced batch renaming capabilities based on custom patterns, sequential numbering, or even image metadata (like EXIF data).
- 🔍 **High-Quality Resizing**: Easy-to-use functions for scaling images while maintaining aspect ratio and image quality.
- 💧 **Watermarking**: A fluent interface to add text or image-based watermarks with control over opacity, position, and tiling.
- 🛠️ **Metadata Management**: The ability to easily read, write, and strip image metadata (EXIF, IPTC, etc.).
- ⚡ **Performance-Focused**: Built on top of highly optimized libraries (like Pillow-SIMD) to ensure speed is a primary feature.

## 🚀 Our Philosophy

- **Simplicity First**: We believe powerful tools don't have to be complicated. Gneiss-Engine features a clean, chainable, and highly readable API.
- **Extensibility**: Designed as a core "engine," it is easy to extend with custom plugins and functionality.
- **Reliability**: A strong focus on comprehensive testing and predictable behavior. It should be the bedrock of your image processing pipeline.

## Installation (Local Development)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gneiss-engine.git
cd gneiss-engine
```

2. Install in development mode:
```bash
pip install -e .
```

This will install the package in "editable" mode, allowing you to modify the code and see changes immediately.

## Usage Example

```python
# The package name is simply 'gneiss' for elegance
from gneiss import Image

# A simple, fluent API for chainable operations
try:
    Image("path/to/source_image.jpg") \
        .resize(width=1024) \
        .add_watermark("logo.png", position="bottom_right", opacity=0.7) \
        .to_format("webp", quality=90) \
        .save("path/to/output/new_image.webp")
    
    print("Image processed successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
```

## How to Contribute

We are not yet accepting pull requests for features, but we are extremely open to ideas and discussions! If you have a suggestion, find a bug in our early code, or want to be a part of the project's future, please open an issue on GitHub.

Your feedback during this crucial initial phase is invaluable.

## License

Distributed under the MIT License. See `LICENSE` file for more information.

## 中文文档

[查看中文文档](README_CN.md)