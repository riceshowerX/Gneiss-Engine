"""
Core Image class for Gneiss-Engine.

This module provides the main Image class that serves as the foundation
for all image manipulation operations in Gneiss-Engine.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

from PIL import Image as PILImage
from PIL import ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from PIL.Image import Resampling


class Image:
    """
    The core Image class for Gneiss-Engine.

    This class provides a fluent interface for image manipulation operations,
    allowing for chainable method calls to perform complex transformations
    with simple, readable code.

    Attributes:
        image (PIL.Image.Image): The underlying PIL Image object.
        path (str): The path to the source image file.
        format (str): The format of the image (e.g., 'JPEG', 'PNG').
        metadata (dict): The metadata associated with the image.
    """

    def __init__(self, source: Union[str, Path, PILImage.Image]):
        """
        Initialize a new Image instance.

        Args:
            source: Path to an image file or a PIL Image object.

        Raises:
            FileNotFoundError: If the source file does not exist.
            ValueError: If the source is not a valid image file or PIL Image object.
        """
        self.path: Optional[str] = None
        self.metadata: Dict[str, Any] = {}
        self.format_params: Dict[str, Any] = {}

        if isinstance(source, (str, Path)):
            source_path = Path(source)
            if not source_path.exists():
                raise FileNotFoundError(f"Image file not found: {source}")

            try:
                self.image = PILImage.open(source_path)
                self.path = str(source_path)
                self.format = self.image.format
                # Extract basic metadata
                self._extract_metadata()
            except Exception as e:
                raise ValueError(f"Could not open image file: {e}")

        elif isinstance(source, PILImage.Image):
            self.image = source
            self.format = source.format

        else:
            raise ValueError("Source must be a file path or a PIL Image object")

    def _extract_metadata(self):
        """Extract metadata from the image."""
        if hasattr(self.image, "info"):
            self.metadata = self.image.info.copy()

        # Extract EXIF data if available
        try:
            exif = self.image._getexif()
            if exif:
                self.metadata["exif"] = exif
        except (AttributeError, Exception):
            # EXIF data not available or not supported
            pass

    def resize(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect: bool = True,
        resample: Resampling = Resampling.LANCZOS,
    ) -> "Image":
        """
        Resize the image to the specified dimensions.

        Args:
            width: The target width in pixels. If None, it will be calculated based on height.
            height: The target height in pixels. If None, it will be calculated based on width.
            maintain_aspect: Whether to maintain the aspect ratio of the original image.
            resample: The resampling filter to use.

        Returns:
            The Image instance for method chaining.

        Raises:
            ValueError: If both width and height are None.
        """
        if width is None and height is None:
            raise ValueError("At least one of width or height must be specified")

        orig_width, orig_height = self.image.size

        # Ensure both dimensions are integers
        final_width = width
        final_height = height

        if maintain_aspect:
            if width is None and height is not None:
                # Calculate width based on height while maintaining aspect ratio
                final_width = int(orig_width * (height / orig_height))
                final_height = height
            elif height is None and width is not None:
                # Calculate height based on width while maintaining aspect ratio
                final_width = width
                final_height = int(orig_height * (width / orig_width))
            elif width is not None and height is not None:
                # Both width and height are specified, but we need to maintain aspect ratio
                # We'll fit the image within the specified dimensions
                ratio = min(width / orig_width, height / orig_height)
                final_width = int(orig_width * ratio)
                final_height = int(orig_height * ratio)
            else:
                # This should not happen due to the initial check
                final_width = orig_width
                final_height = orig_height
        else:
            # If not maintaining aspect ratio, ensure both dimensions are specified
            final_width = width if width is not None else orig_width
            final_height = height if height is not None else orig_height

        self.image = self.image.resize((final_width, final_height), resample=resample)
        return self

    def crop(self, left: int, top: int, right: int, bottom: int) -> "Image":
        """
        Crop the image to the specified rectangle.

        Args:
            left: The left coordinate of the crop rectangle.
            top: The top coordinate of the crop rectangle.
            right: The right coordinate of the crop rectangle.
            bottom: The bottom coordinate of the crop rectangle.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.crop((left, top, right, bottom))
        return self

    def add_watermark(
        self,
        watermark: Union[str, Path, PILImage.Image],
        position: str = "center",
        opacity: float = 0.5,
        padding: int = 10,
    ) -> "Image":
        """
        Add a watermark to the image.

        Args:
            watermark: Path to a watermark image file or a PIL Image object.
            position: The position of the watermark. Options: 'center', 'top_left',
                      'top_right', 'bottom_left', 'bottom_right'.
            opacity: The opacity of the watermark (0.0 to 1.0).
            padding: The padding from the edges in pixels (for non-center positions).

        Returns:
            The Image instance for method chaining.

        Raises:
            ValueError: If the watermark file does not exist or is not a valid image.
        """
        # Load the watermark image
        if isinstance(watermark, (str, Path)):
            watermark_path = Path(watermark)
            if not watermark_path.exists():
                raise FileNotFoundError(f"Watermark file not found: {watermark}")

            try:
                watermark_img = PILImage.open(watermark_path)
            except Exception as e:
                raise ValueError(f"Could not open watermark file: {e}")

        elif isinstance(watermark, PILImage.Image):
            watermark_img = watermark

        else:
            raise ValueError("Watermark must be a file path or a PIL Image object")

        # Convert the watermark to RGBA if it's not already
        if watermark_img.mode != "RGBA":
            watermark_img = watermark_img.convert("RGBA")

        # Apply opacity to the watermark
        if opacity < 1.0:
            alpha = watermark_img.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark_img.putalpha(alpha)

        # Resize watermark if it's larger than the base image
        base_width, base_height = self.image.size
        mark_width, mark_height = watermark_img.size

        if mark_width > base_width or mark_height > base_height:
            # Scale down the watermark to fit within the image
            ratio = (
                min(base_width / mark_width, base_height / mark_height) * 0.8
            )  # 80% of the fitting size
            new_width = int(mark_width * ratio)
            new_height = int(mark_height * ratio)
            watermark_img = watermark_img.resize(
                (new_width, new_height), Resampling.LANCZOS
            )
            mark_width, mark_height = watermark_img.size

        # Create a transparent layer for the watermark
        transparent = PILImage.new("RGBA", self.image.size, (0, 0, 0, 0))

        # Calculate position
        if position == "center":
            x = (base_width - mark_width) // 2
            y = (base_height - mark_height) // 2
        elif position == "top_left":
            x, y = padding, padding
        elif position == "top_right":
            x, y = base_width - mark_width - padding, padding
        elif position == "bottom_left":
            x, y = padding, base_height - mark_height - padding
        elif position == "bottom_right":
            x, y = (
                base_width - mark_width - padding,
                base_height - mark_height - padding,
            )
        else:
            raise ValueError(f"Invalid position: {position}")

        # Paste the watermark onto the transparent layer
        transparent.paste(watermark_img, (x, y), watermark_img)

        # Convert the base image to RGBA if it's not already
        if self.image.mode != "RGBA":
            self.image = self.image.convert("RGBA")

        # Composite the watermark layer with the base image
        self.image = PILImage.alpha_composite(self.image, transparent)

        return self

    def add_text_watermark(
        self,
        text: str,
        position: str = "center",
        font_size: int = 36,
        font_path: Optional[str] = None,
        color: Tuple[int, int, int, int] = (255, 255, 255, 128),
        padding: int = 10,
    ) -> "Image":
        """
        Add a text watermark to the image.

        Args:
            text: The text to add as a watermark.
            position: The position of the watermark. Options: 'center', 'top_left',
                      'top_right', 'bottom_left', 'bottom_right'.
            font_size: The font size in points.
            font_path: Path to a TrueType or OpenType font file. If None, the default font is used.
            color: The color of the text as an RGBA tuple.
            padding: The padding from the edges in pixels (for non-center positions).

        Returns:
            The Image instance for method chaining.
        """
        # Convert the base image to RGBA if it's not already
        if self.image.mode != "RGBA":
            self.image = self.image.convert("RGBA")

        # Create a transparent layer for the text
        txt_layer = PILImage.new("RGBA", self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Load font
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                # Use default font
                font = ImageFont.load_default()
        except Exception as e:
            print(f"Warning: Could not load font, using default. Error: {e}")
            font = ImageFont.load_default()

        # Calculate text size using modern PIL API
        try:
            # Use textbbox for modern Pillow versions (>= 8.0.0)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except (AttributeError, TypeError, Exception):
            # Fallback for older versions or any other error
            # Use a simple estimation based on text length and font size
            text_width = len(text) * font_size // 2
            text_height = font_size

        # Calculate position
        base_width, base_height = self.image.size

        if position == "center":
            x = (base_width - text_width) // 2
            y = (base_height - text_height) // 2
        elif position == "top_left":
            x, y = padding, padding
        elif position == "top_right":
            x, y = base_width - text_width - padding, padding
        elif position == "bottom_left":
            x, y = padding, base_height - text_height - padding
        elif position == "bottom_right":
            x, y = (
                base_width - text_width - padding,
                base_height - text_height - padding,
            )
        else:
            raise ValueError(f"Invalid position: {position}")

        # Draw text
        draw.text((x, y), text, font=font, fill=color)

        # Composite the text layer with the base image
        self.image = PILImage.alpha_composite(self.image, txt_layer)

        return self

    def to_format(self, format_name: str, **kwargs) -> "Image":
        """
        Convert the image to the specified format.

        Args:
            format_name: The target format (e.g., 'JPEG', 'PNG', 'WEBP', 'AVIF').
            **kwargs: Additional format-specific parameters (e.g., quality for JPEG).

        Returns:
            The Image instance for method chaining.

        Raises:
            ValueError: If the format is not supported.
        """
        format_name = format_name.upper()

        # Check if the format is supported
        supported_formats = PILImage.registered_extensions()
        format_extensions = {v: k for k, v in supported_formats.items()}

        if format_name not in format_extensions:
            raise ValueError(f"Unsupported format: {format_name}")

        # Store format-specific parameters
        self.format = format_name
        self.format_params = kwargs  # This will be initialized in save method if needed

        return self

    def save(self, path: Union[str, Path], **kwargs) -> "Image":
        """
        Save the image to the specified path.

        Args:
            path: The path where the image will be saved.
            **kwargs: Additional parameters to pass to PIL's save method.

        Returns:
            The Image instance for method chaining.
        """
        save_path = Path(path)

        # Create directory if it doesn't exist
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Combine format-specific parameters with any additional parameters
        save_params = {}
        if hasattr(self, "format_params"):
            save_params.update(self.format_params)
        save_params.update(kwargs)

        # Save the image
        self.image.save(save_path, format=self.format, **save_params)

        # Update path
        self.path = str(save_path)

        return self

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get the metadata associated with the image.

        Returns:
            A dictionary containing the image metadata.
        """
        # Convert any non-string keys to strings for type consistency
        metadata = {}
        for key, value in self.metadata.items():
            if isinstance(key, (tuple, int)):
                metadata[str(key)] = value
            else:
                metadata[key] = value
        return metadata

    def strip_metadata(self) -> "Image":
        """
        Strip all metadata from the image.

        Returns:
            The Image instance for method chaining.
        """
        # Create a new image without metadata
        new_img = PILImage.new(self.image.mode, self.image.size)
        new_img.paste(self.image)

        self.image = new_img
        self.metadata = {}

        return self

    def rotate(
        self,
        angle: float,
        expand: bool = False,
        resample: Resampling = Resampling.BICUBIC,
        fillcolor: Optional[Tuple[int, ...]] = None,
    ) -> "Image":
        """
        Rotate the image by the specified angle.

        Args:
            angle: The rotation angle in degrees (counter-clockwise).
            expand: Whether to expand the output image to fit the rotated image.
            resample: The resampling filter to use.
            fillcolor: The color to use for areas outside the rotated image.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.rotate(
            angle, resample=resample, expand=expand, fillcolor=fillcolor
        )
        return self

    def flip(self, horizontal: bool = False, vertical: bool = False) -> "Image":
        """
        Flip the image horizontally and/or vertically.

        Args:
            horizontal: Whether to flip the image horizontally.
            vertical: Whether to flip the image vertically.

        Returns:
            The Image instance for method chaining.

        Raises:
            ValueError: If both horizontal and vertical are False.
        """
        if not horizontal and not vertical:
            raise ValueError("At least one of horizontal or vertical must be True")

        if horizontal:
            self.image = ImageOps.mirror(self.image)

        if vertical:
            self.image = ImageOps.flip(self.image)

        return self

    def adjust_brightness(self, factor: float) -> "Image":
        """
        Adjust the brightness of the image.

        Args:
            factor: The brightness adjustment factor.
                   Values > 1.0 increase brightness, values < 1.0 decrease brightness.

        Returns:
            The Image instance for method chaining.
        """
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def adjust_contrast(self, factor: float) -> "Image":
        """
        Adjust the contrast of the image.

        Args:
            factor: The contrast adjustment factor.
                   Values > 1.0 increase contrast, values < 1.0 decrease contrast.

        Returns:
            The Image instance for method chaining.
        """
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def adjust_color(self, factor: float) -> "Image":
        """
        Adjust the color saturation of the image.

        Args:
            factor: The color adjustment factor.
                   Values > 1.0 increase saturation, values < 1.0 decrease saturation.
                   A value of 0.0 produces a grayscale image.

        Returns:
            The Image instance for method chaining.
        """
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def adjust_sharpness(self, factor: float) -> "Image":
        """
        Adjust the sharpness of the image.

        Args:
            factor: The sharpness adjustment factor.
                   Values > 1.0 increase sharpness, values < 1.0 decrease sharpness.

        Returns:
            The Image instance for method chaining.
        """
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def grayscale(self) -> "Image":
        """
        Convert the image to grayscale.

        Returns:
            The Image instance for method chaining.
        """
        self.image = ImageOps.grayscale(self.image)
        return self

    def blur(self, radius: float = 2.0) -> "Image":
        """
        Apply Gaussian blur to the image.

        Args:
            radius: The blur radius. Higher values create more blur.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
        return self

    def sharpen(self, factor: float = 2.0) -> "Image":
        """
        Sharpen the image.

        Args:
            factor: The sharpening factor. Higher values create more sharpening.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.filter(
            ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)
        )
        return self

    def edge_enhance(self) -> "Image":
        """
        Enhance edges in the image.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        return self

    def emboss(self) -> "Image":
        """
        Apply emboss effect to the image.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.filter(ImageFilter.EMBOSS)
        return self

    def contour(self) -> "Image":
        """
        Apply contour effect to the image.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.filter(ImageFilter.CONTOUR)
        return self

    def detail(self) -> "Image":
        """
        Enhance detail in the image.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.filter(ImageFilter.DETAIL)
        return self

    def smooth(self) -> "Image":
        """
        Smooth the image.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.filter(ImageFilter.SMOOTH)
        return self

    def find_edges(self) -> "Image":
        """
        Find and highlight edges in the image.

        Returns:
            The Image instance for method chaining.
        """
        self.image = self.image.filter(ImageFilter.FIND_EDGES)
        return self

    def invert(self) -> "Image":
        """
        Invert the colors of the image.

        Returns:
            The Image instance for method chaining.
        """
        self.image = ImageOps.invert(self.image)
        return self

    def solarize(self, threshold: int = 128) -> "Image":
        """
        Apply solarization effect to the image.

        Args:
            threshold: The solarization threshold.

        Returns:
            The Image instance for method chaining.
        """
        self.image = ImageOps.solarize(self.image, threshold)
        return self

    def posterize(self, bits: int = 4) -> "Image":
        """
        Reduce the number of bits for each color channel.

        Args:
            bits: Number of bits to keep (1-8).

        Returns:
            The Image instance for method chaining.
        """
        self.image = ImageOps.posterize(self.image, bits)
        return self

    def equalize(self) -> "Image":
        """
        Equalize the image histogram.

        Returns:
            The Image instance for method chaining.
        """
        self.image = ImageOps.equalize(self.image)
        return self

    def auto_contrast(
        self, cutoff: float = 0.0, ignore: Optional[int] = None
    ) -> "Image":
        """
        Automatically adjust contrast.

        Args:
            cutoff: Percentage to cut off from histogram.
            ignore: Background pixel value to ignore.

        Returns:
            The Image instance for method chaining.
        """
        self.image = ImageOps.autocontrast(self.image, cutoff=cutoff, ignore=ignore)
        return self

    def colorize(
        self, black_color: Tuple[int, int, int], white_color: Tuple[int, int, int]
    ) -> "Image":
        """
        Colorize a grayscale image.

        Args:
            black_color: RGB color for black points.
            white_color: RGB color for white points.

        Returns:
            The Image instance for method chaining.

        Raises:
            ValueError: If the image is not in grayscale mode.
        """
        if self.image.mode != "L":
            raise ValueError("Colorize operation requires grayscale image (mode 'L')")

        self.image = ImageOps.colorize(self.image, black_color, white_color)
        return self

    def __str__(self) -> str:
        """Return a string representation of the image."""
        width, height = self.image.size
        return (
            f"Image(path='{self.path}', format='{self.format}', size={width}x{height})"
        )

    def __repr__(self) -> str:
        """Return a string representation of the image."""
        return self.__str__()

    def copy(self) -> "Image":
        """Create a copy of the current image instance."""
        return Image(self.image.copy())
