"""
Data models for AI image processing.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class StylePreset:
    """Preset configurations for style transfer."""
    name: str
    prompt: str
    strength: float = 0.8
    guidance_scale: float = 7.5


@dataclass
class GenerationConfig:
    """Configuration for image generation."""
    width: int = 512
    height: int = 512
    num_inference_steps: int = 50
    guidance_scale: float = 7.5
    seed: Optional[int] = None


@dataclass
class DetectionResult:
    """Object detection result."""
    label: str
    confidence: float
    bbox: Tuple[int, int, int, int]
    class_id: int


@dataclass  
class EnhancementConfig:
    """Configuration for image enhancement."""
    scale_factor: int = 2
    denoise_strength: float = 0.5
    sharpen: bool = True
    contrast: float = 1.1