"""
Gneiss Engine Core Module.

This package provides the core functionality for the Gneiss Engine,
including image processing and batch operations.
"""

__version__ = "2.0.0"
__all__ = ["Image", "BatchProcessor", "ImageError"]

from .image import Image, ImageError
from .batch import BatchProcessor

# Enable async support
import asyncio

async def open_image(path: str) -> Image:
    """Async helper to open an image."""
    return await Image.load_async(path)