#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
高级功能使用示例

这个示例展示了 Gneiss-Engine 的一些高级功能，包括：
- 透视变换
- 自适应亮度调整
- 增强的模糊和锐化效果
- 元数据分析和操作
"""

import os
import sys
from typing import Tuple, List

# 添加项目根目录到 Python 路径，以便在开发环境中导入
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gneiss.core import Image, BatchProcessor
from gneiss.utils import file_utils


def demonstrate_perspective_transform():
    """
    演示透视变换功能
    可用于校正倾斜拍摄的文档、建筑照片等
    """
    print("=== 演示透视变换 ===")
    
    try:
        # 打开示例图像
        sample_path = os.path.join(os.path.dirname(__file__), 'sample_images', 'sample1.jpg')
        
        if not os.path.exists(sample_path):
            print(f"警告：示例图像不存在: {sample_path}")
            print("请先运行 create_sample_images.py 生成示例图像")
            return
            
        img = Image.open(sample_path)
        print(f"原始图像尺寸: {img.size}")
        
        # 定义透视变换矩阵
        # 这是一个简单的校正示例，实际应用中需要根据具体情况调整参数
        perspective_data = [
            1.0, 0.05, -20,   # 第一行: a, b, c
            0.03, 1.0, -10,   # 第二行: d, e, f
            0.0001, 0.0001, 1 # 第三行: g, h, i
        ]
        
        # 应用透视变换
        corrected_img = img.perspective_transform(data=perspective_data)
        print("应用透视变换成功")
        
        # 保存结果
        output_path = os.path.join(os.path.dirname(__file__), 'perspective_corrected.jpg')
        corrected_img.save(output_path)
        print(f"透视校正结果已保存至: {output_path}")
        
    except Exception as e:
        print(f"透视变换示例出错: {str(e)}")
    print()


def demonstrate_adaptive_brightness():
    """
    演示自适应亮度调整功能
    根据图像直方图自动调整亮度，保持细节的同时提高可见度
    """
    print("=== 演示自适应亮度调整 ===")
    
    try:
        sample_path = os.path.join(os.path.dirname(__file__), 'sample_images', 'sample2.jpg')
        
        if not os.path.exists(sample_path):
            print(f"警告：示例图像不存在: {sample_path}")
            print("请先运行 create_sample_images.py 生成示例图像")
            return
            
        img = Image.open(sample_path)
        
        # 获取原始亮度统计信息
        original_stats = img.get_brightness_stats()
        print(f"原始图像亮度统计: 平均={original_stats['mean']:.2f}, 最小={original_stats['min']}, 最大={original_stats['max']}")
        
        # 应用自适应亮度调整
        # threshold: 亮度阈值，低于此值的区域会被增强
        # factor: 增强因子，控制调整强度
        adjusted_img = img.adaptive_brightness(threshold=0.3, factor=1.5)
        
        # 获取调整后的亮度统计
        adjusted_stats = adjusted_img.get_brightness_stats()
        print(f"调整后亮度统计: 平均={adjusted_stats['mean']:.2f}, 最小={adjusted_stats['min']}, 最大={adjusted_stats['max']}")
        
        # 保存结果
        output_path = os.path.join(os.path.dirname(__file__), 'adaptive_brightness.jpg')
        adjusted_img.save(output_path)
        print(f"自适应亮度调整结果已保存至: {output_path}")
        
    except Exception as e:
        print(f"自适应亮度调整示例出错: {str(e)}")
    print()


def demonstrate_enhanced_filters():
    """
    演示增强的滤镜效果，包括不同强度的模糊和锐化
    """
    print("=== 演示增强的滤镜效果 ===")
    
    try:
        sample_path = os.path.join(os.path.dirname(__file__), 'sample_images', 'sample3.jpg')
        
        if not os.path.exists(sample_path):
            print(f"警告：示例图像不存在: {sample_path}")
            print("请先运行 create_sample_images.py 生成示例图像")
            return
            
        img = Image.open(sample_path)
        
        # 应用不同强度的高斯模糊
        print("应用低强度模糊 (radius=1)")
        blur_low = img.blur(radius=1)
        blur_low.save(os.path.join(os.path.dirname(__file__), 'blur_low.jpg'))
        
        print("应用中等强度模糊 (radius=3)")
        blur_medium = img.blur(radius=3)
        blur_medium.save(os.path.join(os.path.dirname(__file__), 'blur_medium.jpg'))
        
        print("应用高强度模糊 (radius=5)")
        blur_high = img.blur(radius=5)
        blur_high.save(os.path.join(os.path.dirname(__file__), 'blur_high.jpg'))
        
        # 应用不同强度的锐化
        print("应用低强度锐化 (factor=1.0)")
        sharpen_low = img.sharpen(factor=1.0)
        sharpen_low.save(os.path.join(os.path.dirname(__file__), 'sharpen_low.jpg'))
        
        print("应用中等强度锐化 (factor=2.0)")
        sharpen_medium = img.sharpen(factor=2.0)
        sharpen_medium.save(os.path.join(os.path.dirname(__file__), 'sharpen_medium.jpg'))
        
        print("应用高强度锐化 (factor=3.0)")
        sharpen_high = img.sharpen(factor=3.0)
        sharpen_high.save(os.path.join(os.path.dirname(__file__), 'sharpen_high.jpg'))
        
        print("滤镜效果已保存")
        
    except Exception as e:
        print(f"滤镜效果示例出错: {str(e)}")
    print()


def demonstrate_batch_processing_enhancements():
    """
    演示增强的批量处理功能，包括跳过现有文件、错误处理和进度报告
    """
    print("=== 演示增强的批量处理功能 ===")
    
    try:
        # 获取示例图像路径
        sample_dir = os.path.join(os.path.dirname(__file__), 'sample_images')
        output_dir = os.path.join(os.path.dirname(__file__), 'batch_output')
        
        if not os.path.exists(sample_dir):
            print(f"警告：示例图像目录不存在: {sample_dir}")
            print("请先运行 create_sample_images.py 生成示例图像")
            return
            
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取所有图像文件
        image_paths = file_utils.find_images(sample_dir, extensions=['.jpg', '.png'])
        print(f"找到 {len(image_paths)} 个图像文件")
        
        # 创建批处理器
        processor = BatchProcessor(
            max_workers=2,    # 限制工作线程数
            error_limit=3      # 设置最大错误数
        )
        
        # 定义处理操作：先调整大小，再应用自适应亮度
        def enhance_image(img: Image) -> Image:
            return img.resize(width=600, maintain_aspect=True).adaptive_brightness(threshold=0.4, factor=1.3)
        
        # 执行批量处理，启用跳过现有文件功能
        print("开始批量处理，启用跳过现有文件功能...")
        results = processor.process_images(
            image_paths=image_paths,
            operation=enhance_image,
            output_dir=output_dir,
            output_format="jpg",
            output_suffix="_enhanced",
            show_progress=True,
            skip_existing=True,       # 跳过已存在的输出文件
            stop_on_error=False       # 遇到错误时继续处理
        )
        
        # 显示处理结果统计
        print("\n处理结果统计:")
        metadata = results.get('metadata', {})
        for key, value in metadata.items():
            print(f"  {key}: {value}")
        
        # 显示错误信息
        errors = [(path, result) for path, result in results.items() 
                  if isinstance(result, Exception) and path != 'metadata']
        
        if errors:
            print(f"\n发现 {len(errors)} 个错误:")
            for path, error in errors[:3]:  # 只显示前3个错误
                print(f"  - {path}: {str(error)}")
            if len(errors) > 3:
                print(f"  - ... 以及 {len(errors) - 3} 个其他错误")
        else:
            print("没有遇到错误")
            
    except Exception as e:
        print(f"批量处理示例出错: {str(e)}")
    print()


def demonstrate_thumbnail_creation():
    """
    演示高效的缩略图创建功能
    """
    print("=== 演示缩略图创建 ===")
    
    try:
        sample_path = os.path.join(os.path.dirname(__file__), 'sample_images', 'sample4.png')
        
        if not os.path.exists(sample_path):
            print(f"警告：示例图像不存在: {sample_path}")
            print("请先运行 create_sample_images.py 生成示例图像")
            return
            
        img = Image.open(sample_path)
        print(f"原始图像尺寸: {img.size}")
        
        # 创建不同尺寸的缩略图
        thumbnail_sizes = [(128, 128), (256, 256), (512, 512)]
        
        for size in thumbnail_sizes:
            # 每次创建新副本以避免修改原图
            thumb_img = Image.open(sample_path)
            # 使用缩略图方法（注意：这会修改图像）
            thumb_img.thumbnail(size=size, resample='LANCZOS')
            print(f"创建 {size} 缩略图，实际尺寸: {thumb_img.size}")
            
            # 保存缩略图
            output_path = os.path.join(os.path.dirname(__file__), f'thumbnail_{size[0]}x{size[1]}.jpg')
            thumb_img.save(output_path, quality=85, optimize=True)
            print(f"  已保存至: {output_path}")
            
    except Exception as e:
        print(f"缩略图创建示例出错: {str(e)}")
    print()


def main():
    """
    主函数，运行所有示例
    """
    print("Gneiss-Engine 高级功能示例")
    print("==========================")
    
    # 运行各个演示
    demonstrate_perspective_transform()
    demonstrate_adaptive_brightness()
    demonstrate_enhanced_filters()
    demonstrate_batch_processing_enhancements()
    demonstrate_thumbnail_creation()
    
    print("所有示例运行完成！")
    print("请在 examples 目录下查看生成的结果文件")


if __name__ == "__main__":
    main()
