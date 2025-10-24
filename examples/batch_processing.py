#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
批量处理示例脚本

演示如何使用 Gneiss-Engine 进行图像的批量处理，包括批量调整大小、应用滤镜、格式转换等操作。
同时展示如何处理错误、跳过已存在的文件、显示进度等实用功能。
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Callable

# 导入 Gneiss-Engine 库
sys.path.append(str(Path(__file__).parent.parent))
from gneiss import ImageProcessor
from gneiss.core.batch import BatchProcessor
from gneiss.utils.file_utils import (
    find_images, 
    ensure_directory_exists, 
    get_unique_filename,
    generate_output_filename,
    move_files_with_progress,
    group_files_by_extension,
    get_file_size
)


def show_progress(current: int, total: int) -> None:
    """
    显示处理进度
    
    Args:
        current: 当前处理的文件数
        total: 总文件数
    """
    progress = current / total * 100
    # 使用回车符让进度条在同一行更新
    print(f"进度: {current}/{total} ({progress:.1f}%)", end="\r")
    # 处理完成时换行
    if current == total:
        print()


def print_batch_results(results: Dict[str, Any]) -> None:
    """
    打印批量处理的结果统计
    
    Args:
        results: 包含处理结果的字典
    """
    print("\n处理完成!")
    print(f"成功: {len(results['success'])}")
    
    # 处理不同格式的失败信息
    if 'failed' in results and results['failed']:
        print(f"失败: {len(results['failed'])}")
        print("\n失败的文件:")
        for item in results['failed'][:5]:  # 只显示前5个
            if isinstance(item, tuple) and len(item) >= 2:
                file_path, error_msg = item
                print(f"  - {os.path.basename(file_path)}: {error_msg}")
            elif isinstance(item, dict):
                for file_path, error in item.items():
                    print(f"  - {os.path.basename(file_path)}: {str(error)}")
                    break  # 只显示第一个
        if len(results['failed']) > 5:
            print(f"  ... 以及 {len(results['failed']) - 5} 个其他失败的文件")
    
    # 显示跳过的文件数
    if 'skipped' in results:
        print(f"跳过: {len(results['skipped'])}")


def create_demo_directories() -> tuple:
    """
    创建演示所需的目录
    
    Returns:
        (输入目录, 输出目录) 元组
    """
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    
    # 定义输入和输出目录
    input_dir = script_dir / "sample_images"
    output_dir = script_dir / "processed_images"
    
    # 确保目录存在
    ensure_directory_exists(input_dir)
    ensure_directory_exists(output_dir)
    
    return str(input_dir), str(output_dir)


def traditional_batch_processing(input_dir: str, output_dir: str) -> None:
    """
    使用传统方法进行批量处理（非并行）
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
    """
    print("\n=== 传统批量处理方法 ===")
    print("这种方法使用单线程处理，适合小型批量任务或需要精确控制的场景")
    
    # 批量调整大小函数
    def batch_resize(max_width: int = 800, max_height: int = 600, skip_existing: bool = True):
        # 查找所有图像文件
        image_files = find_images(input_dir)
        if not image_files:
            print(f"在 {input_dir} 中未找到图像文件")
            return
        
        print(f"找到 {len(image_files)} 个图像文件，开始调整大小...")
        
        results = {
            "success": [],
            "failed": [],
            "skipped": []
        }
        
        processor = ImageProcessor()
        
        for i, image_path in enumerate(image_files, 1):
            # 生成输出文件名
            output_path = generate_output_filename(
                image_path, 
                output_dir=output_dir / "resized",
                suffix="_resized"
            )
            
            # 检查文件是否已存在
            if skip_existing and os.path.exists(output_path):
                results["skipped"].append(image_path)
                show_progress(i, len(image_files))
                continue
            
            try:
                # 调整图像大小
                processor.load(image_path)
                processor.resize(max_width=max_width, max_height=max_height, preserve_ratio=True)
                processor.save(output_path)
                results["success"].append((image_path, output_path))
            except Exception as e:
                results["failed"].append((image_path, str(e)))
            
            # 显示进度
            show_progress(i, len(image_files))
        
        return results
    
    # 批量应用滤镜函数
    def batch_apply_filter(filter_name: str, **filter_params):
        # 查找所有图像文件
        image_files = find_images(input_dir)
        if not image_files:
            print(f"在 {input_dir} 中未找到图像文件")
            return
        
        print(f"找到 {len(image_files)} 个图像文件，开始应用 {filter_name} 滤镜...")
        
        results = {
            "success": [],
            "failed": []
        }
        
        processor = ImageProcessor()
        
        for i, image_path in enumerate(image_files, 1):
            # 生成输出文件名
            output_path = generate_output_filename(
                image_path, 
                output_dir=output_dir / f"{filter_name}",
                suffix=f"_{filter_name}"
            )
            
            try:
                # 应用滤镜
                processor.load(image_path)
                
                # 根据滤镜名称调用相应的方法
                if filter_name == "grayscale":
                    processor.to_grayscale()
                elif filter_name == "blur":
                    processor.blur(**filter_params)
                elif filter_name == "sharpen":
                    processor.sharpen(**filter_params)
                elif filter_name == "brightness":
                    processor.adjust_brightness(**filter_params)
                
                processor.save(output_path)
                results["success"].append((image_path, output_path))
            except Exception as e:
                results["failed"].append((image_path, str(e)))
            
            # 显示进度
            show_progress(i, len(image_files))
        
        return results
    
    # 执行示例
    print("\n1. 批量调整图像大小")
    start_time = time.time()
    results = batch_resize(max_width=600, max_height=400)
    end_time = time.time()
    print_batch_results(results)
    print(f"\n耗时: {end_time - start_time:.2f} 秒")
    
    print("\n2. 批量应用灰度滤镜")
    start_time = time.time()
    results = batch_apply_filter("grayscale")
    end_time = time.time()
    print_batch_results(results)
    print(f"\n耗时: {end_time - start_time:.2f} 秒")


def parallel_batch_processing(input_dir: str, output_dir: str) -> None:
    """
    使用BatchProcessor进行并行批量处理
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
    """
    print("\n=== 并行批量处理方法 ===")
    print("这种方法使用BatchProcessor类进行并行处理，适合大型批量任务")
    
    # 获取所有图像文件
    image_paths = find_images(input_dir)
    if not image_paths:
        print(f"在 {input_dir} 中未找到图像文件")
        return
    
    print(f"找到 {len(image_paths)} 个图像文件")
    
    # 创建BatchProcessor实例
    batch_processor = BatchProcessor()
    
    # 示例1: 格式转换
    print("\n=== 示例1: 批量转换为WEBP格式 ===")
    try:
        start_time = time.time()
        results = batch_processor.convert_format(
            image_paths=image_paths,
            output_format="WEBP",
            output_dir=output_dir / "webp_converted",
            quality=90,
            show_progress=True,
            skip_existing=True
        )
        end_time = time.time()
        
        # 处理结果
        success_count = sum(1 for result in results.values() if not isinstance(result, Exception))
        failed_count = len(results) - success_count
        
        print(f"成功: {success_count}")
        print(f"失败: {failed_count}")
        print(f"耗时: {end_time - start_time:.2f} 秒")
        
    except Exception as e:
        print(f"批量转换出错: {e}")
    
    # 示例2: 调整大小
    print("\n=== 示例2: 批量调整大小 ===")
    try:
        start_time = time.time()
        results = batch_processor.resize_images(
            image_paths=image_paths,
            width=800,
            height=600,
            maintain_aspect=True,
            output_dir=output_dir / "batch_resized",
            show_progress=True,
            skip_existing=True
        )
        end_time = time.time()
        
        success_count = sum(1 for result in results.values() if not isinstance(result, Exception))
        failed_count = len(results) - success_count
        
        print(f"成功: {success_count}")
        print(f"失败: {failed_count}")
        print(f"耗时: {end_time - start_time:.2f} 秒")
        
    except Exception as e:
        print(f"批量调整大小出错: {e}")
    
    # 示例3: 添加水印
    print("\n=== 示例3: 批量添加水印 ===")
    try:
        start_time = time.time()
        results = batch_processor.add_text_watermark_to_images(
            image_paths=image_paths,
            text="Gneiss-Engine",
            position="bottom_right",
            font_size=24,
            color=(255, 255, 255, 180),  # 白色半透明
            output_dir=output_dir / "watermarked",
            show_progress=True,
            skip_existing=True
        )
        end_time = time.time()
        
        success_count = sum(1 for result in results.values() if not isinstance(result, Exception))
        failed_count = len(results) - success_count
        
        print(f"成功: {success_count}")
        print(f"失败: {failed_count}")
        print(f"耗时: {end_time - start_time:.2f} 秒")
        
    except Exception as e:
        print(f"批量添加水印出错: {e}")
    
    # 示例4: 自定义处理
    print("\n=== 示例4: 自定义批量处理 ===")
    try:
        def custom_operation(img):
            """自定义处理操作"""
            return (
                img.resize(width=1000, maintain_aspect=True)
                .adjust_brightness(1.1)
                .adjust_contrast(1.2)
                .add_text_watermark(
                    text="Processed by Gneiss",
                    position="bottom_right",
                    font_size=18,
                    color=(255, 255, 255, 150)
                )
            )
        
        start_time = time.time()
        results = batch_processor.process_images(
            image_paths=image_paths,
            operation=custom_operation,
            output_dir=output_dir / "custom_processed",
            output_format="JPEG",
            output_suffix="_enhanced",
            show_progress=True,
            skip_existing=True
        )
        end_time = time.time()
        
        success_count = sum(1 for result in results.values() if not isinstance(result, Exception))
        failed_count = len(results) - success_count
        
        print(f"成功: {success_count}")
        print(f"失败: {failed_count}")
        print(f"耗时: {end_time - start_time:.2f} 秒")
        
    except Exception as e:
        print(f"自定义批量处理出错: {e}")


def batch_format_conversion(input_dir: str, output_dir: str) -> None:
    """
    批量格式转换专用功能
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
    """
    print("\n=== 批量格式转换工具 ===")
    
    # 获取所有图像文件
    image_paths = find_images(input_dir)
    if not image_paths:
        print(f"在 {input_dir} 中未找到图像文件")
        return
    
    # 按格式分组显示统计信息
    grouped_by_ext = group_files_by_extension(image_paths)
    print("\n文件格式统计:")
    for ext, files in grouped_by_ext.items():
        print(f"  {ext.upper()}: {len(files)} 个文件")
    
    # 格式选择
    format_map = {
        "1": "JPG",
        "2": "PNG",
        "3": "WEBP",
        "4": "TIFF",
        "5": "BMP"
    }
    
    print("\n目标格式选项:")
    for key, fmt in format_map.items():
        print(f"  {key}. {fmt}")
    
    choice = input("请选择目标格式 (1-5): ")
    if choice not in format_map:
        print("无效的选择")
        return
    
    output_format = format_map[choice]
    
    # 质量设置
    if output_format in ["JPG", "WEBP"]:
        try:
            quality = int(input("请输入质量 (1-100, 默认 90): ") or "90")
            quality = max(1, min(100, quality))  # 限制在有效范围内
        except ValueError:
            quality = 90
    else:
        quality = 90
    
    # 输出目录
    format_output_dir = output_dir / f"{output_format.lower()}_converted"
    
    # 开始转换
    print(f"\n开始将 {len(image_paths)} 个文件转换为 {output_format} 格式...")
    
    batch_processor = BatchProcessor()
    try:
        start_time = time.time()
        results = batch_processor.convert_format(
            image_paths=image_paths,
            output_format=output_format,
            output_dir=format_output_dir,
            quality=quality,
            show_progress=True,
            skip_existing=True
        )
        end_time = time.time()
        
        success_count = sum(1 for result in results.values() if not isinstance(result, Exception))
        
        print(f"\n转换完成!")
        print(f"成功: {success_count} 个文件")
        print(f"失败: {len(results) - success_count} 个文件")
        print(f"耗时: {end_time - start_time:.2f} 秒")
        print(f"输出目录: {format_output_dir}")
        
        # 显示文件大小统计
        if success_count > 0:
            total_original_size = 0
            total_new_size = 0
            for img_path in image_paths:
                if img_path in results and not isinstance(results[img_path], Exception):
                    total_original_size += get_file_size(img_path)
                    total_new_size += get_file_size(results[img_path])
            
            if total_original_size > 0:
                ratio = (total_new_size / total_original_size) * 100
                print(f"\n文件大小统计:")
                print(f"  原始总大小: {get_file_size(total_original_size, human_readable=True)}")
                print(f"  新文件总大小: {get_file_size(total_new_size, human_readable=True)}")
                print(f"  压缩率: {ratio:.1f}%")
                
    except Exception as e:
        print(f"转换过程出错: {e}")


def custom_batch_workflow(input_dir: str, output_dir: str) -> None:
    """
    自定义批量工作流
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
    """
    print("\n=== 自定义批量工作流 ===")
    print("创建一个包含多个处理步骤的工作流")
    
    # 获取所有图像文件
    image_paths = find_images(input_dir)
    if not image_paths:
        print(f"在 {input_dir} 中未找到图像文件")
        return
    
    print(f"找到 {len(image_paths)} 个图像文件")
    
    # 定义工作流选项
    workflow_steps = []
    
    # 步骤1: 调整大小
    resize_choice = input("\n是否调整大小? (y/n, 默认 y): ").lower()
    if resize_choice != "n":
        try:
            width = int(input("请输入宽度 (默认 800): ") or "800")
            height = int(input("请输入高度 (默认 600): ") or "600")
            maintain_aspect = input("保持纵横比? (y/n, 默认 y): ").lower() != "n"
            
            def resize_step(img):
                return img.resize(width=width, height=height, maintain_aspect=maintain_aspect)
            
            workflow_steps.append(("调整大小", resize_step))
        except ValueError:
            print("无效的数值，跳过调整大小")
    
    # 步骤2: 调整亮度和对比度
    enhance_choice = input("\n是否调整亮度和对比度? (y/n, 默认 n): ").lower() == "y"
    if enhance_choice:
        try:
            brightness = float(input("请输入亮度系数 (0.1-3.0, 默认 1.1): ") or "1.1")
            contrast = float(input("请输入对比度系数 (0.1-3.0, 默认 1.2): ") or "1.2")
            
            def enhance_step(img):
                return img.adjust_brightness(brightness).adjust_contrast(contrast)
            
            workflow_steps.append(("增强亮度对比度", enhance_step))
        except ValueError:
            print("无效的数值，跳过增强步骤")
    
    # 步骤3: 添加水印
    watermark_choice = input("\n是否添加水印? (y/n, 默认 n): ").lower() == "y"
    if watermark_choice:
        watermark_text = input("请输入水印文本: ") or "Processed"
        position = input("水印位置 (top_left/top_right/bottom_left/bottom_right/center, 默认 bottom_right): ") or "bottom_right"
        
        try:
            font_size = int(input("字体大小 (默认 24): ") or "24")
            opacity = float(input("透明度 (0-1, 默认 0.5): ") or "0.5")
            
            def watermark_step(img):
                return img.add_text_watermark(
                    text=watermark_text,
                    position=position,
                    font_size=font_size,
                    color=(255, 255, 255, int(opacity * 255))
                )
            
            workflow_steps.append(("添加水印", watermark_step))
        except ValueError:
            print("无效的数值，使用默认水印设置")
            
            def watermark_step(img):
                return img.add_text_watermark(
                    text=watermark_text,
                    position=position,
                    font_size=24,
                    color=(255, 255, 255, 128)
                )
            
            workflow_steps.append(("添加水印", watermark_step))
    
    # 如果没有选择任何步骤
    if not workflow_steps:
        print("未选择任何处理步骤，退出")
        return
    
    # 定义完整的工作流函数
    def workflow(img):
        for name, step in workflow_steps:
            img = step(img)
        return img
    
    # 执行工作流
    print("\n处理步骤:")
    for i, (name, _) in enumerate(workflow_steps, 1):
        print(f"  {i}. {name}")
    
    # 输出设置
    output_suffix = input("\n输出文件名后缀 (默认 '_processed'): ") or "_processed"
    output_format_choice = input("输出格式 (jpg/png/webp, 默认保持原格式): ").lower() or None
    
    batch_processor = BatchProcessor()
    workflow_output_dir = output_dir / "workflow_processed"
    
    print(f"\n开始执行工作流，处理 {len(image_paths)} 个文件...")
    
    try:
        start_time = time.time()
        results = batch_processor.process_images(
            image_paths=image_paths,
            operation=workflow,
            output_dir=workflow_output_dir,
            output_format=output_format_choice.upper() if output_format_choice else None,
            output_suffix=output_suffix,
            show_progress=True,
            skip_existing=True
        )
        end_time = time.time()
        
        success_count = sum(1 for result in results.values() if not isinstance(result, Exception))
        
        print(f"\n工作流执行完成!")
        print(f"成功: {success_count} 个文件")
        print(f"失败: {len(results) - success_count} 个文件")
        print(f"耗时: {end_time - start_time:.2f} 秒")
        print(f"输出目录: {workflow_output_dir}")
        
    except Exception as e:
        print(f"工作流执行出错: {e}")


def main():
    """
    主函数，运行批量处理演示
    """
    print("Gneiss-Engine 批量处理示例")
    print("========================")
    print()
    print("此脚本展示了Gneiss-Engine的多种批量处理功能，包括:")
    print("- 传统单线程批量处理")
    print("- 并行批量处理 (使用BatchProcessor)")
    print("- 批量格式转换工具")
    print("- 自定义处理工作流")
    print()
    
    # 创建演示目录
    input_dir, output_dir = create_demo_directories()
    output_dir = Path(output_dir)
    
    # 检查示例图像是否存在
    sample_images = find_images(input_dir)
    if not sample_images:
        print(f"警告: 在 {input_dir} 中未找到示例图像")
        print("请先运行 create_sample_images.py 生成示例图像")
        print()
    else:
        print(f"找到 {len(sample_images)} 个示例图像")
    
    print("\n批量处理功能菜单:")
    print("1. 传统批量处理示例")
    print("2. 并行批量处理示例")
    print("3. 批量格式转换工具")
    print("4. 自定义处理工作流")
    print("0. 退出")
    
    while True:
        try:
            choice = input("\n请选择要执行的功能 (0-4): ")
            
            if choice == "0":
                print("\n感谢使用Gneiss-Engine批量处理工具!")
                break
                
            elif choice == "1":
                traditional_batch_processing(input_dir, output_dir)
                
            elif choice == "2":
                parallel_batch_processing(input_dir, output_dir)
                
            elif choice == "3":
                batch_format_conversion(input_dir, output_dir)
                
            elif choice == "4":
                custom_batch_workflow(input_dir, output_dir)
                
            else:
                print("无效的选择，请输入 0-4 之间的数字")
                
            # 询问是否继续
            if input("\n按Enter键继续，输入'q'退出: ").lower() == "q":
                break
                
        except KeyboardInterrupt:
            print("\n\n操作被用户中断")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
            
            if input("\n按Enter键继续，输入'q'退出: ").lower() == "q":
                break


if __name__ == "__main__":
    main()
