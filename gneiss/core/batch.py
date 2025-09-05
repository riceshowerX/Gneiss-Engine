 """
Batch processing functionality for Gneiss-Engine.

This module provides tools for processing multiple images in batch operations.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union

from tqdm import tqdm

from gneiss.core.image import Image


class BatchProcessor:
    """
    A class for batch processing multiple images.

    This class provides methods for applying operations to multiple images
    in parallel, with progress tracking and error handling.
    """

    def __init__(self, max_workers: int = None):
        """
        Initialize a new BatchProcessor instance.

        Args:
            max_workers: The maximum number of worker threads to use.
                         If None, it will use the default from ThreadPoolExecutor.
        """
        self.max_workers = max_workers

    def process_images(
        self,
        image_paths: List[Union[str, Path]],
        operation: Callable[[Image], Image],
        output_dir: Optional[Union[str, Path]] = None,
        output_format: Optional[str] = None,
        output_suffix: str = "_processed",
        show_progress: bool = True,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Process multiple images with the given operation.

        Args:
            image_paths: List of paths to the images to process.
            operation: A function that takes an Image object and
                       returns a processed Image object.
            output_dir: Directory where processed images will be saved.
                       If None, images will be saved in the same
                       directory as the input images.
            output_format: Format to save the processed images in.
                          If None, the original format is used.
            output_suffix: Suffix to add to the output filenames.
            show_progress: Whether to show a progress bar.

        Returns:
            A dictionary mapping input paths to output paths or exceptions.
        """
        results = {}

        # Create output directory if it doesn't exist
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        # Define the processing function
        def process_single_image(image_path):
            try:
                # Load the image
                img = Image(image_path)

                # Apply the operation
                processed_img = operation(img)

                # Determine output path
                input_path = Path(image_path)

                if output_dir:
                    # Use the specified output directory
                    stem = input_path.stem + output_suffix
                    if output_format:
                        # Use the specified format
                        ext = f".{output_format.lower()}"
                    else:
                        # Use the original format
                        ext = input_path.suffix

                    output_path = output_dir / f"{stem}{ext}"
                else:
                    # Save in the same directory as the input
                    stem = input_path.stem + output_suffix
                    if output_format:
                        # Use the specified format
                        ext = f".{output_format.lower()}"
                    else:
                        # Use the original format
                        ext = input_path.suffix

                    output_path = input_path.parent / f"{stem}{ext}"

                # Save the processed image
                if output_format:
                    processed_img.to_format(output_format)

                processed_img.save(output_path)

                return str(image_path), str(output_path)

            except Exception as e:
                return str(image_path), e

        # Process images in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(process_single_image, path) for path in image_paths
            ]

            if show_progress:
                for future in tqdm(
                    as_completed(futures), total=len(futures), desc="Processing images"
                ):
                    input_path, result = future.result()
                    results[input_path] = result
            else:
                for future in as_completed(futures):
                    input_path, result = future.result()
                    results[input_path] = result

        return results

    def convert_format(
        self,
        image_paths: List[Union[str, Path]],
        output_format: str,
        output_dir: Optional[Union[str, Path]] = None,
        quality: int = 90,
        show_progress: bool = True,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Convert multiple images to a different format.

        Args:
            image_paths: List of paths to the images to convert.
            output_format: Format to convert the images to (e.g., 'JPEG', 'PNG', 'WEBP').
            output_dir: Directory where converted images will be saved.
                       If None, images will be saved in the same directory as the input images.
            quality: Quality setting for the output format (if applicable).
            show_progress: Whether to show a progress bar.

        Returns:
            A dictionary mapping input paths to output paths or exceptions.
        """

        # Define the conversion operation
        def convert_operation(img):
            return img.to_format(output_format, quality=quality)

        return self.process_images(
            image_paths=image_paths,
            operation=convert_operation,
            output_dir=output_dir,
            output_format=output_format,
            output_suffix="",  # No suffix for format conversion
            show_progress=show_progress,
        )

    def resize_images(
        self,
        image_paths: List[Union[str, Path]],
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect: bool = True,
        output_dir: Optional[Union[str, Path]] = None,
        output_format: Optional[str] = None,
        show_progress: bool = True,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Resize multiple images.

        Args:
            image_paths: List of paths to the images to resize.
            width: Target width in pixels. If None, it will be calculated based on height.
            height: Target height in pixels. If None, it will be calculated based on width.
            maintain_aspect: Whether to maintain the aspect ratio of the original images.
            output_dir: Directory where resized images will be saved.
                       If None, images will be saved in the same directory as the input images.
            output_format: Format to save the resized images in. If None, the original format is used.
            show_progress: Whether to show a progress bar.

        Returns:
            A dictionary mapping input paths to output paths or exceptions.
        """

        # Define the resize operation
        def resize_operation(img):
            return img.resize(
                width=width, height=height, maintain_aspect=maintain_aspect
            )

        return self.process_images(
            image_paths=image_paths,
            operation=resize_operation,
            output_dir=output_dir,
            output_format=output_format,
            output_suffix="_resized",
            show_progress=show_progress,
        )

    def add_watermark_to_images(
        self,
        image_paths: List[Union[str, Path]],
        watermark: Union[str, Path, Image],
        position: str = "center",
        opacity: float = 0.5,
        padding: int = 10,
        output_dir: Optional[Union[str, Path]] = None,
        output_format: Optional[str] = None,
        show_progress: bool = True,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Add a watermark to multiple images.

        Args:
            image_paths: List of paths to the images to watermark.
            watermark: Path to a watermark image file or an Image object.
            position: The position of the watermark. Options: 'center', 
                      'top_left', 'top_right', 'bottom_left', 'bottom_right'.
            opacity: The opacity of the watermark (0.0 to 1.0).
            padding: The padding from the edges in pixels 
                     (for non-center positions).
            output_dir: Directory where watermarked images will be saved. If None, images will be saved
                       in the same directory as the input images.
            output_format: Format to save the watermarked images in. If None, the original format is used.
            show_progress: Whether to show a progress bar.

        Returns:
            A dictionary mapping input paths to output paths or exceptions.
        """

        # Define the watermark operation
        def watermark_operation(img):
            return img.add_watermark(
                watermark=watermark, position=position, opacity=opacity, padding=padding
            )

        return self.process_images(
            image_paths=image_paths,
            operation=watermark_operation,
            output_dir=output_dir,
            output_format=output_format,
            output_suffix="_watermarked",
            show_progress=show_progress,
        )

    def add_text_watermark_to_images(
        self,
        image_paths: List[Union[str, Path]],
        text: str,
        position: str = "center",
        font_size: int = 36,
        font_path: Optional[str] = None,
        color: Tuple[int, int, int, int] = (255, 255, 255, 128),
        padding: int = 10,
        output_dir: Optional[Union[str, Path]] = None,
        output_format: Optional[str] = None,
        show_progress: bool = True,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Add a text watermark to multiple images.

        Args:
            image_paths: List of paths to the images to watermark.
            text: The text to add as a watermark.
            position: The position of the watermark. Options: 'center', 'top_left',
                      'top_right', 'bottom_left', 'bottom_right'.
            font_size: The font size in points.
            font_path: Path to a TrueType or OpenType font file. If None, the default font is used.
            color: The color of the text as an RGBA tuple.
            padding: The padding from the edges in pixels (for non-center positions).
            output_dir: Directory where watermarked images will be saved. If None, images will be saved
                       in the same directory as the input images.
            output_format: Format to save the watermarked images in. If None, the original format is used.
            show_progress: Whether to show a progress bar.

        Returns:
            A dictionary mapping input paths to output paths or exceptions.
        """

        # Define the text watermark operation
        def text_watermark_operation(img):
            return img.add_text_watermark(
                text=text,
                position=position,
                font_size=font_size,
                font_path=font_path,
                color=color,
                padding=padding,
            )

        return self.process_images(
            image_paths=image_paths,
            operation=text_watermark_operation,
            output_dir=output_dir,
            output_format=output_format,
            output_suffix="_text_watermarked",
            show_progress=show_progress,
        )

    def strip_metadata_from_images(
        self,
        image_paths: List[Union[str, Path]],
        output_dir: Optional[Union[str, Path]] = None,
        output_format: Optional[str] = None,
        show_progress: bool = True,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Strip metadata from multiple images.

        Args:
            image_paths: List of paths to the images to process.
            output_dir: Directory where processed images will be saved. If None, images will be saved
                       in the same directory as the input images.
            output_format: Format to save the processed images in. If None, the original format is used.
            show_progress: Whether to show a progress bar.

        Returns:
            A dictionary mapping input paths to output paths or exceptions.
        """

        # Define the strip metadata operation
        def strip_metadata_operation(img):
            return img.strip_metadata()

        return self.process_images(
            image_paths=image_paths,
            operation=strip_metadata_operation,
            output_dir=output_dir,
            output_format=output_format,
            output_suffix="_no_metadata",
            show_progress=show_progress,
        )
