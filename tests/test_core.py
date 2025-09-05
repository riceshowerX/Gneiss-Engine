"""
Tests for core image processing functionality.
"""

import asyncio
import tempfile
from pathlib import Path

import pytest
from PIL import Image as PILImage

from gneiss.core import Image, ImageError


class TestImage:
    """Test Image class functionality."""
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample test image."""
        img = PILImage.new('RGB', (100, 100), color='red')
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            img.save(tmp.name, format='JPEG')
            yield tmp.name
            Path(tmp.name).unlink()
    
    @pytest.mark.asyncio
    async def test_image_creation(self, sample_image):
        """Test image creation from file path."""
        image = Image(sample_image)
        assert image.path == sample_image
        assert image.format == 'JPEG'
        assert image.width == 100
        assert image.height == 100
    
    @pytest.mark.asyncio
    async def test_async_loading(self, sample_image):
        """Test async image loading."""
        image = await Image.load_async(sample_image)
        assert image.path == sample_image
        assert image.width == 100
    
    @pytest.mark.asyncio
    async def test_resize(self, sample_image):
        """Test image resizing."""
        image = Image(sample_image)
        resized = await image.resize_async(50, 50)
        
        assert resized.width == 50
        assert resized.height == 50
        assert resized.image.size == (50, 50)
    
    @pytest.mark.asyncio
    async def test_crop(self, sample_image):
        """Test image cropping."""
        image = Image(sample_image)
        cropped = image.crop(10, 10, 90, 90)
        
        assert cropped.width == 80
        assert cropped.height == 80
    
    def test_invalid_file(self):
        """Test error handling for invalid files."""
        with pytest.raises(ImageError):
            Image("nonexistent.jpg")
    
    @pytest.mark.asyncio
    async def test_metadata_extraction(self, sample_image):
        """Test metadata extraction."""
        image = Image(sample_image)
        metadata = image.get_metadata()
        
        assert isinstance(metadata, dict)
        assert 'exif' in metadata or 'custom' in metadata
    
    @pytest.mark.asyncio
    async def test_format_conversion(self, sample_image):
        """Test image format conversion."""
        image = Image(sample_image)
        converted = image.to_format('PNG')
        
        assert converted.format == 'PNG'
    
    @pytest.mark.asyncio
    async def test_grayscale_conversion(self, sample_image):
        """Test grayscale conversion."""
        image = Image(sample_image)
        grayscale = image.grayscale()
        
        assert grayscale.image.mode == 'L'
    
    @pytest.mark.asyncio
    async def test_brightness_adjustment(self, sample_image):
        """Test brightness adjustment."""
        image = Image(sample_image)
        adjusted = image.adjust_brightness(1.5)
        
        assert adjusted is not None
    
    @pytest.mark.asyncio
    async def test_contrast_adjustment(self, sample_image):
        """Test contrast adjustment."""
        image = Image(sample_image)
        adjusted = image.adjust_contrast(1.5)
        
        assert adjusted is not None
    
    @pytest.mark.asyncio
    async def test_save_image(self, sample_image):
        """Test image saving."""
        image = Image(sample_image)
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            saved = await image.save_async(tmp.name)
            assert Path(tmp.name).exists()
            assert saved.path == tmp.name


class TestImageErrorHandling:
    """Test error handling scenarios."""
    
    def test_nonexistent_file(self):
        """Test loading nonexistent file."""
        with pytest.raises(ImageError):
            Image("/nonexistent/image.jpg")
    
    def test_invalid_image_data(self):
        """Test loading invalid image data."""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
            tmp.write(b"invalid image data")
            tmp.flush()
            
            with pytest.raises(ImageError):
                Image(tmp.name)
    
    @pytest.mark.asyncio
    async def test_async_error_handling(self):
        """Test async error handling."""
        with pytest.raises(ImageError):
            await Image.load_async("/nonexistent/image.jpg")


@pytest.mark.performance
class TestImagePerformance:
    """Performance tests for image operations."""
    
    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_resize_performance(self, sample_image, benchmark):
        """Benchmark resize performance."""
        image = Image(sample_image)
        
        def resize_op():
            return image.resize(50, 50)
        
        # Run benchmark
        result = benchmark(resize_op)
        assert result.width == 50
    
    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_async_resize_performance(self, sample_image, benchmark):
        """Benchmark async resize performance."""
        image = Image(sample_image)
        
        async def async_resize():
            return await image.resize_async(50, 50)
        
        # Run benchmark
        result = await benchmark(async_resize)
        assert result.width == 50