"""
Metadata utility functions for Gneiss-Engine.

This module provides functions for working with image metadata,
including EXIF, IPTC, and XMP data.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def extract_exif(image_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Extract EXIF metadata from an image file.

    Args:
        image_path: Path to the image file.

    Returns:
        A dictionary containing the EXIF metadata with human-readable tags.
    """
    try:
        with Image.open(image_path) as img:
            exif_data = {}

            if hasattr(img, "_getexif") and callable(img._getexif):
                exif = img._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)

                        # Handle GPS data specially
                        if tag == "GPSInfo":
                            gps_data = {}
                            for gps_tag_id, gps_value in value.items():
                                gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                                gps_data[gps_tag] = gps_value
                            exif_data[tag] = gps_data
                        else:
                            exif_data[tag] = value

            return exif_data
    except Exception as e:
        print(f"Error extracting EXIF data: {e}")
        return {}


def get_image_metadata(image_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Get comprehensive metadata from an image file.

    Args:
        image_path: Path to the image file.

    Returns:
        A dictionary containing all available metadata.
    """
    metadata = {"basic": {}, "exif": {}, "iptc": {}, "xmp": {}}

    try:
        with Image.open(image_path) as img:
            # Basic metadata
            metadata["basic"] = {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height,
                "info": img.info,
            }

            # EXIF data
            metadata["exif"] = extract_exif(image_path)

            # Extract IPTC data if available
            try:
                from PIL import IptcImagePlugin
                iptc_data = IptcImagePlugin.getiptcinfo(img)
                if iptc_data:
                    metadata["iptc"] = iptc_data
            except (ImportError, Exception):
                pass

            # Extract XMP data if available
            try:
                from libxmp import XMPFiles
                xmp_file = XMPFiles(file_path=str(image_path))
                xmp_data = xmp_file.get_xmp()
                if xmp_data:
                    metadata["xmp"] = xmp_data
                xmp_file.close_file()
            except (ImportError, Exception):
                pass

            return metadata
    except Exception as e:
        print(f"Error getting image metadata: {e}")
        return metadata


def get_creation_date(image_path: Union[str, Path]) -> Optional[str]:
    """
    Extract the creation date from image metadata.

    Args:
        image_path: Path to the image file.

    Returns:
        The creation date as a string, or None if not available.
    """
    exif_data = extract_exif(image_path)

    # Try different EXIF tags that might contain the date
    date_tags = ["DateTimeOriginal", "DateTimeDigitized", "DateTime"]

    for tag in date_tags:
        if tag in exif_data:
            return exif_data[tag]

    return None


def get_gps_coordinates(image_path: Union[str, Path]) -> Optional[Dict[str, float]]:
    """
    Extract GPS coordinates from image metadata.

    Args:
        image_path: Path to the image file.

    Returns:
        A dictionary with 'latitude' and 'longitude' keys, or None if not available.
    """
    exif_data = extract_exif(image_path)

    if "GPSInfo" not in exif_data:
        return None

    gps_info = exif_data["GPSInfo"]

    # Check if we have the required GPS data
    if "GPSLatitude" not in gps_info or "GPSLongitude" not in gps_info:
        return None

    # Convert GPS coordinates from degrees/minutes/seconds to decimal degrees
    def convert_to_decimal(value, ref):
        degrees, minutes, seconds = value
        decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        if ref in ["S", "W"]:
            decimal = -decimal
        return decimal

    try:
        latitude = convert_to_decimal(
            gps_info["GPSLatitude"], gps_info.get("GPSLatitudeRef", "N")
        )
        longitude = convert_to_decimal(
            gps_info["GPSLongitude"], gps_info.get("GPSLongitudeRef", "E")
        )

        return {"latitude": latitude, "longitude": longitude}
    except Exception as e:
        print(f"Error converting GPS coordinates: {e}")
        return None


def strip_all_metadata(
    image_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None
) -> bool:
    """
    Strip all metadata from an image file.

    Args:
        image_path: Path to the input image file.
        output_path: Path where the stripped image will be saved. If None, overwrites the original.

    Returns:
        True if successful, False otherwise.
    """
    if output_path is None:
        output_path = image_path

    try:
        # Open the image
        with Image.open(image_path) as img:
            # Create a new image with the same content but without metadata
            data = list(img.getdata())
            new_img = Image.new(img.mode, img.size)
            new_img.putdata(data)

            # Save the new image
            new_img.save(output_path)

            return True
    except Exception as e:
        print(f"Error stripping metadata: {e}")
        return False


def copy_metadata(source_path: Union[str, Path], target_path: Union[str, Path]) -> bool:
    """
    Copy metadata from one image to another.

    Args:
        source_path: Path to the source image (metadata donor).
        target_path: Path to the target image (metadata recipient).

    Returns:
        True if successful, False otherwise.
    """
    try:
        # This is a simplified version that only works with EXIF data
        # A more comprehensive solution would require additional libraries

        # Extract metadata from source
        with Image.open(source_path) as source_img:
            if not hasattr(source_img, "_getexif") or not callable(source_img._getexif):
                return False

            exif_data = source_img._getexif()
            if not exif_data:
                return False

        # Open target image
        with Image.open(target_path) as target_img:
            # Create a new image with the target content
            data = list(target_img.getdata())
            new_img = Image.new(target_img.mode, target_img.size)
            new_img.putdata(data)

            # Save with the source metadata
            new_img.save(target_path, exif=exif_data)

            return True
    except Exception as e:
        print(f"Error copying metadata: {e}")
        return False
