#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件工具模块

提供文件和目录相关的实用功能，如查找图像文件、获取文件信息、批量操作等。
"""

import os
import re
import shutil
import fnmatch
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union


def get_files_by_extension(
    directory: Union[str, Path], extensions: List[str], recursive: bool = True
) -> List[Path]:
    """
    Get all files with the specified extensions in the directory.

    Args:
        directory: The directory to search in.
        extensions: List of file extensions to include (e.g., ['.jpg', '.png']).
        recursive: Whether to search recursively in subdirectories.

    Returns:
        A list of Path objects for the matching files.
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Normalize extensions to lowercase with leading dot
    normalized_extensions = [
        ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions
    ]

    result = []

    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in normalized_extensions:
                    result.append(file_path)
    else:
        for file in directory.iterdir():
            if file.is_file() and file.suffix.lower() in normalized_extensions:
                result.append(file)

    return result


def batch_rename(
    files: List[Union[str, Path]],
    pattern: str,
    replacement: str,
    use_regex: bool = False,
) -> Dict[str, str]:
    """
    Rename multiple files based on a pattern.

    Args:
        files: List of file paths to rename.
        pattern: The pattern to search for in the filename.
        replacement: The replacement string.
        use_regex: Whether to use regex for pattern matching.

    Returns:
        A dictionary mapping original filenames to new filenames.

    Example:
        >>> files = ['img001.jpg', 'img002.jpg']
        >>> batch_rename(files, 'img', 'photo')
        {'img001.jpg': 'photo001.jpg', 'img002.jpg': 'photo002.jpg'}
    """
    result = {}

    for file_path in files:
        file_path = Path(file_path)
        original_name = file_path.name
        parent_dir = file_path.parent

        if use_regex:
            new_name = re.sub(pattern, replacement, original_name)
        else:
            new_name = original_name.replace(pattern, replacement)

        new_path = parent_dir / new_name

        # Store the mapping without actually renaming
        result[str(file_path)] = str(new_path)

    return result


def apply_rename(rename_map: Dict[str, str]) -> Dict[str, bool]:
    """
    Apply the renaming based on a rename map.

    Args:
        rename_map: A dictionary mapping original filenames to new filenames.

    Returns:
        A dictionary indicating success/failure for each file.
    """
    result = {}

    for original, new in rename_map.items():
        original_path = Path(original)
        new_path = Path(new)

        try:
            # Check if the destination already exists
            if new_path.exists():
                result[original] = False
                continue

            # Rename the file
            original_path.rename(new_path)
            result[original] = True
        except Exception:
            result[original] = False

    return result


def generate_sequential_names(
    directory: Union[str, Path],
    base_name: str,
    extension: str,
    start_number: int = 1,
    padding: int = 3,
) -> List[str]:
    """
    Generate sequential filenames for a directory.

    Args:
        directory: The directory to generate names for.
        base_name: The base name for the files.
        extension: The file extension.
        start_number: The starting number for the sequence.
        padding: The number of digits to pad the sequence number with.

    Returns:
        A list of generated filenames.

    Example:
        >>> generate_sequential_names('.', 'img', 'jpg', 1, 3)
        ['img001.jpg', 'img002.jpg', ...]
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Normalize extension
    if not extension.startswith("."):
        extension = f".{extension}"

    # Get existing files to determine how many files to generate
    existing_files = list(directory.iterdir())
    file_count = len([f for f in existing_files if f.is_file()])

    # Generate sequential names
    result = []
    for i in range(start_number, start_number + file_count):
        filename = f"{base_name}{str(i).zfill(padding)}{extension}"
        result.append(filename)

    return result


def find_images(directory: Union[str, Path], 
                extensions: Optional[List[str]] = None, 
                recursive: bool = True) -> List[str]:
    """
    在指定目录中查找图像文件
    
    Args:
        directory: 要搜索的目录路径
        extensions: 要查找的文件扩展名列表，默认为常见图像格式
        recursive: 是否递归搜索子目录
        
    Returns:
        找到的图像文件的绝对路径列表
    """
    # 默认支持的图像格式
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    
    # 确保扩展名都以点开头
    normalized_extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    # 转换为小写以实现大小写不敏感的匹配
    normalized_extensions = [ext.lower() for ext in normalized_extensions]
    
    image_paths = []
    directory = str(directory)
    
    if not os.path.isdir(directory):
        raise ValueError(f"指定的目录不存在或不是目录: {directory}")
    
    if recursive:
        # 递归搜索
        for root, _, files in os.walk(directory):
            for file in files:
                _, ext = os.path.splitext(file.lower())
                if ext in normalized_extensions:
                    full_path = os.path.abspath(os.path.join(root, file))
                    image_paths.append(full_path)
    else:
        # 仅搜索顶层目录
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path):
                _, ext = os.path.splitext(item.lower())
                if ext in normalized_extensions:
                    image_paths.append(os.path.abspath(full_path))
    
    # 按路径排序，使结果更稳定
    image_paths.sort()
    
    return image_paths


def get_unique_filename(base_path: Union[str, Path], suffix: str = '') -> str:
    """
    生成唯一的文件名，避免覆盖现有文件
    
    如果指定的文件名已存在，会在文件名后添加序号
    
    Args:
        base_path: 基础文件路径
        suffix: 要添加到文件名的后缀（在扩展名之前）
        
    Returns:
        唯一的文件路径
    """
    base_path = str(base_path)
    
    # 分离文件名和扩展名
    dir_path, filename = os.path.split(base_path)
    name_without_ext, ext = os.path.splitext(filename)
    
    # 如果有后缀，添加到文件名中
    if suffix:
        name_without_ext = f"{name_without_ext}{suffix}"
    
    # 构建新的文件路径
    new_path = os.path.join(dir_path, f"{name_without_ext}{ext}")
    
    # 如果文件已存在，添加序号
    counter = 1
    while os.path.exists(new_path):
        new_path = os.path.join(dir_path, f"{name_without_ext}_{counter}{ext}")
        counter += 1
    
    return new_path


def ensure_directory_exists(path: Union[str, Path]) -> None:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        path: 目录路径
    """
    directory = str(path)
    
    # 如果是文件路径，获取其目录部分
    if os.path.splitext(directory)[1]:  # 检查是否有扩展名
        directory = os.path.dirname(directory)
    
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def split_path_by_extension(path: Union[str, Path]) -> tuple:
    """
    将文件路径分割为基本路径和扩展名（考虑多部分扩展名）
    
    Args:
        path: 文件路径
        
    Returns:
        (base_path, extension) 元组，其中 extension 包含点号
    """
    path_str = str(path)
    
    # 处理特殊情况
    if not path_str:
        return "", ""
    
    # 多部分扩展名映射
    multi_part_extensions = {
        '.tar.gz', '.tar.bz2', '.tar.xz', '.tar.Z', 
        '.tar.lzma', '.tar.br', '.tar.lz4', '.tar.zst'
    }
    
    # 尝试匹配多部分扩展名
    for multi_ext in sorted(multi_part_extensions, key=len, reverse=True):
        if path_str.lower().endswith(multi_ext):
            base = path_str[:-len(multi_ext)]
            return base, multi_ext
    
    # 标准扩展名处理
    base, ext = os.path.splitext(path_str)
    return base, ext


def get_file_size(path: Union[str, Path], human_readable: bool = False) -> Union[int, str]:
    """
    获取文件大小
    
    Args:
        path: 文件路径
        human_readable: 是否返回人类可读的大小（如 1.5MB）
        
    Returns:
        文件大小（字节数或人类可读字符串）
    """
    path_str = str(path)
    
    if not os.path.isfile(path_str):
        raise ValueError(f"指定的路径不是文件: {path_str}")
    
    size_bytes = os.path.getsize(path_str)
    
    if not human_readable:
        return size_bytes
    
    # 转换为人类可读格式
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f}{unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f}PB"


def filter_files_by_pattern(file_list: List[str], patterns: List[str]) -> List[str]:
    """
    根据通配符模式过滤文件列表
    
    Args:
        file_list: 文件路径列表
        patterns: 通配符模式列表（如 ['*.jpg', '*.png']）
        
    Returns:
        匹配任何模式的文件路径列表
    """
    matched_files = []
    
    for file_path in file_list:
        filename = os.path.basename(file_path)
        for pattern in patterns:
            if fnmatch.fnmatch(filename, pattern):
                matched_files.append(file_path)
                break  # 一个文件只需要匹配一个模式
    
    return matched_files


def group_files_by_extension(file_list: List[str]) -> dict:
    """
    按文件扩展名对文件列表进行分组
    
    Args:
        file_list: 文件路径列表
        
    Returns:
        字典，键为扩展名（小写），值为该扩展名的文件列表
    """
    grouped = {}
    
    for file_path in file_list:
        _, ext = os.path.splitext(file_path.lower())
        if ext not in grouped:
            grouped[ext] = []
        grouped[ext].append(file_path)
    
    return grouped


def remove_files(file_paths: List[str], skip_missing: bool = True) -> tuple:
    """
    删除文件列表中的所有文件
    
    Args:
        file_paths: 要删除的文件路径列表
        skip_missing: 是否跳过不存在的文件
        
    Returns:
        (成功删除的文件数, 失败的文件路径列表)
    """
    success_count = 0
    failed_paths = []
    
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                success_count += 1
            elif not skip_missing:
                failed_paths.append(file_path)
        except Exception:
            failed_paths.append(file_path)
    
    return success_count, failed_paths


def move_files_with_progress(source_paths: List[str], 
                             destination_dir: str, 
                             on_progress=None) -> dict:
    """
    将文件移动到目标目录，并支持进度回调
    
    Args:
        source_paths: 源文件路径列表
        destination_dir: 目标目录
        on_progress: 进度回调函数，接收参数 (current, total)
        
    Returns:
        包含成功和失败移动的文件信息的字典
    """
    ensure_directory_exists(destination_dir)
    
    results = {
        'success': [],
        'failed': []
    }
    
    total = len(source_paths)
    
    for i, source_path in enumerate(source_paths):
        destination_path = os.path.join(destination_dir, os.path.basename(source_path))
        
        try:
            # 确保目标文件不存在
            if os.path.exists(destination_path):
                destination_path = get_unique_filename(destination_path)
            
            shutil.move(source_path, destination_path)
            results['success'].append((source_path, destination_path))
        except Exception as e:
            results['failed'].append((source_path, str(e)))
        
        # 调用进度回调
        if on_progress:
            on_progress(i + 1, total)
    
    return results


def generate_output_filename(input_path: Union[str, Path], 
                            output_dir: Optional[Union[str, Path]] = None, 
                            output_format: Optional[str] = None,
                            suffix: Optional[str] = None) -> str:
    """
    生成输出文件名
    
    Args:
        input_path: 输入文件路径
        output_dir: 输出目录，默认为输入文件所在目录
        output_format: 输出格式（不含点号），默认为输入文件格式
        suffix: 要添加到文件名的后缀（在扩展名之前）
        
    Returns:
        生成的输出文件路径
    """
    input_path = str(input_path)
    
    # 获取输入文件信息
    input_dir, input_filename = os.path.split(input_path)
    input_name, input_ext = os.path.splitext(input_filename)
    input_ext = input_ext[1:].lower()  # 移除点号并转为小写
    
    # 确定输出目录
    if output_dir is None:
        output_dir = input_dir
    else:
        output_dir = str(output_dir)
        ensure_directory_exists(output_dir)
    
    # 确定输出格式
    format_to_use = output_format if output_format is not None else input_ext
    
    # 构建新文件名
    new_filename = input_name
    if suffix:
        new_filename = f"{new_filename}{suffix}"
    new_filename = f"{new_filename}.{format_to_use.lower()}"
    
    # 组合完整路径
    output_path = os.path.join(output_dir, new_filename)
    
    # 确保文件名唯一
    return get_unique_filename(output_path)


# 如果作为主程序运行，展示功能示例
if __name__ == "__main__":
    import sys
    
    # 示例用法
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        print(f"在 {directory} 中查找图像文件...")
        images = find_images(directory)
        print(f"找到 {len(images)} 个图像文件:")
        for img in images[:5]:  # 只显示前5个
            print(f"  - {img}")
        if len(images) > 5:
            print(f"  ... 以及 {len(images) - 5} 个其他文件")
    else:
        print("使用方法: python file_utils.py <目录路径>")

