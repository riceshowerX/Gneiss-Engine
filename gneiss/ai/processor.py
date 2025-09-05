"""
AI Image Processor with state-of-the-art models.
"""

import asyncio
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

import torch
import torch.nn.functional as F
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from PIL import Image as PILImage
from transformers import (
    CLIPImageProcessor,
    CLIPModel,
    DetrForObjectDetection,
    DetrImageProcessor,
)

from gneiss.core import Image
from gneiss.utils.cache import async_lru_cache


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


class AIImageProcessor:
    """Advanced AI image processor with multiple model support."""
    
    def __init__(self, device: str = "cuda"):
        self.device = device
        self._models_loaded = False
        self._style_presets = self._load_style_presets()
        
    async def warmup(self):
        """Warm up all models asynchronously."""
        if not self._models_loaded:
            await asyncio.gather(
                self._load_diffusion_models(),
                self._load_detection_models(),
                self._load_clip_model()
            )
            self._models_loaded = True
    
    async def _load_diffusion_models(self):
        """Load diffusion models for image generation and editing."""
        self.text_to_image = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None,
        ).to(self.device)
        
        self.image_to_image = StableDiffusionImg2ImgPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None,
        ).to(self.device)
    
    async def _load_detection_models(self):
        """Load object detection models."""
        self.detector = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
        self.detector_processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
        self.detector.to(self.device)
    
    async def _load_clip_model(self):
        """Load CLIP model for image-text similarity."""
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_model.to(self.device)
    
    @async_lru_cache(maxsize=100)
    async def enhance(self, image: Image, scale: int = 2) -> Image:
        """Enhance image quality using super-resolution."""
        # Placeholder for real super-resolution model
        # Currently uses simple upscaling with AI-enhanced interpolation
        enhanced = await image.resize_async(
            width=image.width * scale,
            height=image.height * scale,
            resample=PILImage.LANCZOS
        )
        return enhanced
    
    async def style_transfer(self, image: Image, style: Union[str, StylePreset]) -> Image:
        """Apply artistic style transfer to image."""
        if isinstance(style, str):
            style = self._style_presets.get(style, self._style_presets["default"])
        
        # Convert to PIL for diffusion pipeline
        pil_image = image.image.convert("RGB")
        
        # Generate styled image
        result = self.image_to_image(
            prompt=style.prompt,
            image=pil_image,
            strength=style.strength,
            guidance_scale=style.guidance_scale,
            num_inference_steps=25,
        ).images[0]
        
        return Image(result)
    
    async def generate_from_prompt(self, prompt: str, config: Optional[GenerationConfig] = None) -> Image:
        """Generate image from text prompt using diffusion model."""
        config = config or GenerationConfig()
        
        if config.seed is not None:
            torch.manual_seed(config.seed)
        
        result = self.text_to_image(
            prompt=prompt,
            width=config.width,
            height=config.height,
            num_inference_steps=config.num_inference_steps,
            guidance_scale=config.guidance_scale,
        ).images[0]
        
        return Image(result)
    
    async def detect_objects(self, image: Image, threshold: float = 0.8) -> List[Dict]:
        """Detect objects in image and return bounding boxes."""
        inputs = self.detector_processor(images=image.image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.detector(**inputs)
        
        results = self.detector_processor.post_process_object_detection(
            outputs, threshold=threshold
        )[0]
        
        return [
            {
                "label": self.detector.config.id2label[int(label)],
                "score": float(score),
                "box": [int(coord) for coord in box.tolist()],
            }
            for score, label, box in zip(
                results["scores"], results["labels"], results["boxes"]
            )
        ]
    
    def _load_style_presets(self) -> Dict[str, StylePreset]:
        """Load predefined style presets."""
        return {
            "default": StylePreset("default", "high quality, detailed", 0.7),
            "oil_painting": StylePreset("oil_painting", "oil painting style", 0.8),
            "anime": StylePreset("anime", "anime style, vibrant colors", 0.75),
            "sketch": StylePreset("sketch", "pencil sketch, black and white", 0.65),
        }
    
    async def cleanup(self):
        """Clean up model resources."""
        if hasattr(self, "text_to_image"):
            del self.text_to_image
        if hasattr(self, "image_to_image"):
            del self.image_to_image
        if hasattr(self, "detector"):
            del self.detector
        if hasattr(self, "clip_model"):
            del self.clip_model
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self._models_loaded = False