"""
Batch processing functionality for Gneiss-Engine.

This module provides tools for processing multiple images in batch operations.
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from tqdm import tqdm

from gneiss.core.image import Image


class BatchProcessor:
    """
    A class for batch processing multiple images.

    This class provides methods for applying operations to multiple images
    in parallel, with progress tracking and error handling. It includes smart worker pool
    management and detailed error handling.
    """

    def __init__(self, max_workers: int = None, max_errors: int = 10):
        """
        Initialize a new BatchProcessor instance.

        Args:
            max_workers: The maximum number of worker threads to use.
                         If None, it will dynamically adjust based on system load.
            max_errors: Maximum number of errors to report in detail before summarizing.
        """
        self.max_workers = max_workers if max_workers is not None else self._calculate_optimal_workers()
        self.max_errors = max_errors
        self._active_jobs = 0
        self._error_count = 0

    def _calculate_optimal_workers(self) -> int:
        """
        Calculate the optimal number of worker threads based on system resources.

        Returns:
            The calculated number of workers.
        """
        import os
        import psutil

        try:
            cpu_count = os.cpu_count() or 4
            
            # Get available memory (in GB)
            available_memory_gb = psutil.virtual_memory().available / (1024 ** 3)
            
            # For image processing, we typically want to use most CPU cores but leave some headroom
            # and also consider available memory to prevent swapping
            optimal_workers = min(
                cpu_count,
                max(1, int(available_memory_gb / 2))  # At least 2GB per worker
            )
            
            cpu_load = psutil.cpu_percent(interval=1) / 100
            
            # Adjust workers based on CPU load and leave at least 1 core free
            if cpu_load < 0.5:
                return min(optimal_workers, cpu_count - 1)  # Leave at least 1 core free
            elif cpu_load < 0.8:
                return max(1, cpu_count - 1)  # Always leave at least 1 core
            else:
                return max(1, (cpu_count - 1) // 2)  # Reduce workers if CPU is busy
        except (ImportError, AttributeError):
            # Fallback to CPU count - 1 if system resource detection fails
            cpu_count = os.cpu_count() or 4
            return max(1, cpu_count - 1)

    def process_images(
        self,
        image_paths: List[Union[str, Path]],
        operation: Callable[[Image], Image],
        output_dir: Optional[Union[str, Path]] = None,
        output_format: Optional[str] = None,
        output_suffix: str = "_processed",
        show_progress: bool = True,
        skip_existing: bool = False,
        stop_on_error: bool = False,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Process multiple images in parallel with enhanced error handling and resource management.

        Args:
            image_paths: List of paths to the images to process.
            operation: A function that takes an Image object and returns a processed Image object.
            output_dir: Directory where processed images will be saved. If None, images will be saved
                       in the same directory as the input images.
            output_format: Format to save the processed images in. If None, the original format is used.
            output_suffix: Suffix to add to the output filenames.
            show_progress: Whether to show a progress bar.
            skip_existing: Whether to skip images that already have a processed output file.
            stop_on_error: Whether to stop processing at the first error encountered.

        Returns:
            Dict mapping input paths to output paths or exceptions, with additional metadata.
        """
        # Validate input
        valid_paths = []
        for path in image_paths:
            path_str = str(path)
            if not os.path.exists(path_str):
                print(f"Warning: Image file not found: {path_str}")
                continue
            if not os.path.isfile(path_str):
                print(f"Warning: Not a file: {path_str}")
                continue
            valid_paths.append(path_str)
        
        if not valid_paths:
            raise ValueError("No valid image files found in the input list")

        # Create output directory if it doesn't exist
        output_dir_path = Path(output_dir) if output_dir else None
        if output_dir_path:
            output_dir_path.mkdir(parents=True, exist_ok=True)

        # Helper function to get output path
        def get_output_path(image_path):
            input_path = Path(image_path)
            stem = input_path.stem + output_suffix
            if output_format:
                ext = f".{output_format.lower()}"
            else:
                ext = input_path.suffix
            
            if output_dir_path:
                return output_dir_path / f"{stem}{ext}"
            else:
                return input_path.parent / f"{stem}{ext}"

        # Define the processing function
        def process_single_image(image_path):
            try:
                # Load the image
                img = Image(image_path)

                # Apply the operation
                processed_img = operation(img)

                # Determine output path
                output_path = get_output_path(image_path)

                # Save the processed image
                if output_format:
                    processed_img.to_format(output_format)

                processed_img.save(output_path)

                return str(image_path), str(output_path)

            except Exception as e:
                return str(image_path), e

        # Results dictionary and error tracking
        results = {}
        self._error_count = 0
        skipped_count = 0

        # Process images in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tasks
            futures = []
            future_to_path = {}
            
            # Pre-check for existing files if skip_existing is True
            for path in valid_paths:
                if skip_existing:
                    output_path = get_output_path(path)
                    if os.path.exists(output_path):
                        results[path] = str(output_path)
                        skipped_count += 1
                        continue
                
                future = executor.submit(process_single_image, path)
                futures.append(future)
                future_to_path[future] = path
            
            # Process results
            if show_progress:
                for future in tqdm(
                    as_completed(futures), total=len(futures), desc="Processing images"
                ):
                    path = future_to_path[future]
                    try:
                        input_path, result = future.result()
                        
                        # Check if result is an exception
                        if isinstance(result, Exception):
                            self._error_count += 1
                            # Provide detailed error information for the first few errors
                            if self._error_count <= self.max_errors:
                                detailed_error = f"Error processing {path}: {str(result)} (Type: {type(result).__name__})"
                                results[path] = RuntimeError(detailed_error)
                            else:
                                # For subsequent errors, use a summary
                                results[path] = RuntimeError(f"Error processing {path} (see detailed logs)")
                            
                            # Stop processing if stop_on_error is True
                            if stop_on_error:
                                executor.shutdown(wait=False, cancel_futures=True)
                                print(f"Processing stopped due to error. {self._error_count} error(s) encountered.")
                                break
                        else:
                            results[path] = result
                        
                        # Update progress bar with statistics
                        success_count = len(results) - skipped_count - self._error_count
                        tqdm.write(f"Progress: {success_count} success, {self._error_count} errors, {skipped_count} skipped")
                        
                    except Exception as e:
                        # This handles exceptions during future.result()
                        self._error_count += 1
                        results[path] = RuntimeError(f"Fatal error processing {path}: {str(e)}")
                        if stop_on_error:
                            executor.shutdown(wait=False, cancel_futures=True)
                            print(f"Processing stopped due to fatal error. {self._error_count} error(s) encountered.")
                            break
            else:
                for future in as_completed(futures):
                    path = future_to_path[future]
                    try:
                        input_path, result = future.result()
                        
                        if isinstance(result, Exception):
                            self._error_count += 1
                            if self._error_count <= self.max_errors:
                                detailed_error = f"Error processing {path}: {str(result)} (Type: {type(result).__name__})"
                                results[path] = RuntimeError(detailed_error)
                            else:
                                results[path] = RuntimeError(f"Error processing {path} (see detailed logs)")
                            
                            if stop_on_error:
                                executor.shutdown(wait=False, cancel_futures=True)
                                print(f"Processing stopped due to error. {self._error_count} error(s) encountered.")
                                break
                        else:
                            results[path] = result
                    except Exception as e:
                        self._error_count += 1
                        results[path] = RuntimeError(f"Fatal error processing {path}: {str(e)}")
                        if stop_on_error:
                            executor.shutdown(wait=False, cancel_futures=True)
                            print(f"Processing stopped due to fatal error. {self._error_count} error(s) encountered.")
                            break
        
        # Add metadata to results
        success_count = len(results) - skipped_count - self._error_count
        success_rate = success_count / len(valid_paths) if valid_paths else 0
        
        results['_metadata'] = {
            'total_input': len(image_paths),
            'valid_input': len(valid_paths),
            'processed': success_count + self._error_count,
            'skipped': skipped_count,
            'errors': self._error_count,
            'success': success_count,
            'success_rate': success_rate
        }

        return results

    def convert_format(
        self,
        image_paths: List[Union[str, Path]],
        output_format: str,
        output_dir: Optional[Union[str, Path]] = None,
        quality: int = 90,
        show_progress: bool = True,
        skip_existing: bool = False,
        stop_on_error: bool = False,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Convert multiple images to a different format with enhanced options.

        Args:
            image_paths: List of paths to the images to convert.
            output_format: Format to convert the images to (e.g., 'JPEG', 'PNG', 'WEBP').
            output_dir: Directory where converted images will be saved. If None, images will be saved
                       in the same directory as the input images.
            quality: Quality setting for the output format (if applicable).
            show_progress: Whether to show a progress bar.
            skip_existing: Whether to skip images that already have a converted output file.
            stop_on_error: Whether to stop processing at the first error encountered.

        Returns:
            A dictionary mapping input paths to output paths or exceptions, with additional metadata.
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
            skip_existing=skip_existing,
            stop_on_error=stop_on_error,
        )

    def resize_images(
        self,
        image_paths: List[Union[str, Path]],
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect: bool = True,
        output_dir: Optional[Union[str, Path]] = None,
        output_format: Optional[str] = None,
        output_suffix: str = "_resized",
        show_progress: bool = True,
        skip_existing: bool = False,
        stop_on_error: bool = False,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Resize multiple images with enhanced options.

        Args:
            image_paths: List of paths to the images to resize.
            width: Target width in pixels. If None, it will be calculated based on height.
            height: Target height in pixels. If None, it will be calculated based on width.
            maintain_aspect: Whether to maintain the aspect ratio of the original images.
            output_dir: Directory where resized images will be saved. If None, images will be saved
                       in the same directory as the input images.
            output_format: Format to save the resized images in. If None, the original format is used.
            output_suffix: Suffix to add to output filenames.
            show_progress: Whether to show a progress bar.
            skip_existing: Whether to skip images that already have a resized output file.
            stop_on_error: Whether to stop processing at the first error encountered.

        Returns:
            A dictionary mapping input paths to output paths or exceptions, with additional metadata.
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
            output_suffix=output_suffix,
            show_progress=show_progress,
            skip_existing=skip_existing,
            stop_on_error=stop_on_error,
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
        skip_existing: bool = False,
        stop_on_error: bool = False,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Add a watermark to multiple images.

        Args:
            image_paths: List of paths to the images to watermark.
            watermark: Path to a watermark image file or an Image object.
            position: The position of the watermark. Options: 'center', 'top_left',
                      'top_right', 'bottom_left', 'bottom_right'.
            opacity: The opacity of the watermark (0.0 to 1.0).
            padding: The padding from the edges in pixels (for non-center positions).
            output_dir: Directory where watermarked images will be saved. If None, images will be saved
                       in the same directory as the input images.
            output_format: Format to save the watermarked images in. If None, the original format is used.
            show_progress: Whether to show a progress bar.
            skip_existing: Whether to skip images that already have a watermarked output file.
            stop_on_error: Whether to stop processing at the first error encountered.

        Returns:
            A dictionary mapping input paths to output paths or exceptions, with additional metadata.
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
            skip_existing=skip_existing,
            stop_on_error=stop_on_error,
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
        skip_existing: bool = False,
        stop_on_error: bool = False,
    ) -> Dict[str, Union[str, Exception]]:
        """
        Strip metadata from multiple images.

        Args:
            image_paths: List of paths to the images to process.
            output_dir: Directory where processed images will be saved. If None, images will be saved
                       in the same directory as the input images.
            output_format: Format to save the processed images in. If None, the original format is used.
            show_progress: Whether to show a progress bar.
            skip_existing: Whether to skip images that already have a processed output file.
            stop_on_error: Whether to stop processing at the first error encountered.

        Returns:
            A dictionary mapping input paths to output paths or exceptions, with additional metadata.
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
            skip_existing=skip_existing,
            stop_on_error=stop_on_error,
        )
