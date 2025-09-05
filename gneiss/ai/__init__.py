"""
AI-powered image processing module for Gneiss Engine.

This module provides advanced AI capabilities including:
- Image enhancement and super-resolution
- Style transfer and artistic filters
- Object detection and segmentation
- Image generation using diffusion models
"""

from .processor import AIImageProcessor
from .models import StylePreset, GenerationConfig

__all__ = ["AIImageProcessor", "StylePreset", "GenerationConfig"]