"""
Gneiss-Engine 高级图像处理示例

此脚本演示了 Gneiss-Engine 中更高级的图像处理功能，包括：
- 图像增强和修复技术
- 边缘检测和轮廓提取
- 图像分割
- 高级滤镜应用
- 自定义图像处理函数
- 性能优化技术
"""

import os
import sys
import time
from pathlib import Path
import numpy as np
from typing import List, Dict, Tuple, Optional, Union

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

# 导入Gneiss-Engine库
from gneiss import ImageProcessor
from gneiss.processing.enhance import (
    enhance_details,
    adaptive_contrast,
    smart_denoise,
    unsharp_masking,
    equalize_histogram
)
from gneiss.processing.detect import (
    detect_edges,
    detect_faces,
    find_contours,
    detect_corners
)
from gneiss.processing.transform import (
    perspective_transform,
    rotate_image,
    flip_image,
    crop_to_content
)
from gneiss.processing.filters import (
    apply_custom_filter,
    apply_blur,
    apply_sharpen,
    apply_sobel_filter,
    apply_canny_edge_detection
)
from gneiss.processing.color import (
    adjust_hue_saturation,
    color_balance,
    selective_color,
    convert_to_grayscale,
    apply_sepia
)
from gneiss.processing.segment import (
    segment_by_threshold,
    kmeans_segmentation,
    watershed_segmentation
)


def print_header(title: str) -> None:
    """打印带分隔线的标题"""
    print("\n" + "=" * 70)
    print(f" {title} ".center(70, "="))
    print("=" * 70)


def get_sample_image_path() -> Optional[Path]:
    """
    获取示例图像路径
    
    Returns:
        示例图像路径或None（如果未找到）
    """
    current_dir = Path(__file__).parent
    sample_dir = current_dir / "sample_images"
    
    # 查找第一个可用的图像文件
    image_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    
    for ext in image_extensions:
        images = list(sample_dir.glob(f"*{ext}"))
        if images:
            return images[0]
    
    # 检查子目录
    for subdir in sample_dir.iterdir():
        if subdir.is_dir():
            for ext in image_extensions:
                images = list(subdir.glob(f"*{ext}"))
                if images:
                    return images[0]
    
    return None


def demo_image_enhancement():
    """演示高级图像增强技术"""
    print_header("1. 高级图像增强技术")
    
    # 获取示例图像
    image_path = get_sample_image_path()
    if not image_path:
        print("错误: 未找到示例图像")
        print("请先运行: python examples/create_sample_images.py")
        return
    
    print(f"使用示例图像: {image_path.name}")
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "processed_images" / "enhancement"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建图像处理器
    processor = ImageProcessor()
    processor.load(image_path)
    
    # 显示原始图像信息
    print(f"\n原始图像: {image_path.name}")
    print(f"尺寸: {processor.width}x{processor.height}")
    print(f"模式: {processor.mode}")
    
    # 1. 细节增强
    print("\n1.1 应用细节增强...")
    detail_enhanced = processor.copy()
    enhance_details(detail_enhanced, strength=1.2)
    detail_output = output_dir / f"{image_path.stem}_detail_enhanced{image_path.suffix}"
    detail_enhanced.save(detail_output)
    print(f"保存细节增强图像: {detail_output}")
    
    # 2. 自适应对比度
    print("\n1.2 应用自适应对比度增强...")
    adaptive_contrast_img = processor.copy()
    adaptive_contrast(adaptive_contrast_img, clip_limit=2.0, tile_grid_size=(8, 8))
    adaptive_output = output_dir / f"{image_path.stem}_adaptive_contrast{image_path.suffix}"
    adaptive_contrast_img.save(adaptive_output)
    print(f"保存自适应对比度图像: {adaptive_output}")
    
    # 3. 智能降噪
    print("\n1.3 应用智能降噪...")
    denoised_img = processor.copy()
    smart_denoise(denoised_img, strength=0.6)
    denoised_output = output_dir / f"{image_path.stem}_denoised{image_path.suffix}"
    denoised_img.save(denoised_output)
    print(f"保存降噪图像: {denoised_output}")
    
    # 4. 非锐化遮罩
    print("\n1.4 应用非锐化遮罩...")
    unsharp_img = processor.copy()
    unsharp_masking(unsharp_img, radius=1.5, amount=1.2, threshold=1)
    unsharp_output = output_dir / f"{image_path.stem}_unsharp{image_path.suffix}"
    unsharp_img.save(unsharp_output)
    print(f"保存非锐化图像: {unsharp_output}")
    
    # 5. 直方图均衡化
    print("\n1.5 应用直方图均衡化...")
    equalized_img = processor.copy()
    equalize_histogram(equalized_img)
    equalized_output = output_dir / f"{image_path.stem}_equalized{image_path.suffix}"
    equalized_img.save(equalized_output)
    print(f"保存直方图均衡化图像: {equalized_output}")
    
    print(f"\n所有增强图像已保存到: {output_dir}")


def demo_edge_detection_and_segmentation():
    """演示边缘检测和图像分割技术"""
    print_header("2. 边缘检测和图像分割")
    
    # 获取示例图像
    image_path = get_sample_image_path()
    if not image_path:
        print("错误: 未找到示例图像")
        print("请先运行: python examples/create_sample_images.py")
        return
    
    print(f"使用示例图像: {image_path.name}")
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "processed_images" / "segmentation"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建图像处理器
    processor = ImageProcessor()
    processor.load(image_path)
    
    # 1. Canny边缘检测
    print("\n2.1 应用Canny边缘检测...")
    canny_edges = processor.copy()
    apply_canny_edge_detection(canny_edges, low_threshold=50, high_threshold=150)
    canny_output = output_dir / f"{image_path.stem}_canny_edges.png"
    canny_edges.save(canny_output)
    print(f"保存Canny边缘检测图像: {canny_output}")
    
    # 2. Sobel滤镜
    print("\n2.2 应用Sobel边缘检测...")
    sobel_edges = processor.copy()
    apply_sobel_filter(sobel_edges)
    sobel_output = output_dir / f"{image_path.stem}_sobel_edges.png"
    sobel_edges.save(sobel_output)
    print(f"保存Sobel边缘检测图像: {sobel_output}")
    
    # 3. 阈值分割
    print("\n2.3 应用阈值分割...")
    threshold_segmented = processor.copy()
    segment_by_threshold(threshold_segmented, threshold=128)
    threshold_output = output_dir / f"{image_path.stem}_threshold_segmented.png"
    threshold_segmented.save(threshold_output)
    print(f"保存阈值分割图像: {threshold_output}")
    
    # 4. K-means聚类分割
    print("\n2.4 应用K-means聚类分割...")
    kmeans_segmented = processor.copy()
    kmeans_segmentation(kmeans_segmented, k=5)
    kmeans_output = output_dir / f"{image_path.stem}_kmeans_segmented{image_path.suffix}"
    kmeans_segmented.save(kmeans_output)
    print(f"保存K-means分割图像: {kmeans_output}")
    
    # 5. 分水岭分割
    print("\n2.5 应用分水岭分割...")
    watershed_segmented = processor.copy()
    watershed_segmentation(watershed_segmented, markers=50)
    watershed_output = output_dir / f"{image_path.stem}_watershed_segmented{image_path.suffix}"
    watershed_segmented.save(watershed_output)
    print(f"保存分水岭分割图像: {watershed_output}")
    
    print(f"\n所有分割图像已保存到: {output_dir}")


def demo_advanced_color_processing():
    """演示高级色彩处理技术"""
    print_header("3. 高级色彩处理")
    
    # 获取示例图像
    image_path = get_sample_image_path()
    if not image_path:
        print("错误: 未找到示例图像")
        print("请先运行: python examples/create_sample_images.py")
        return
    
    print(f"使用示例图像: {image_path.name}")
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "processed_images" / "color_processing"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建图像处理器
    processor = ImageProcessor()
    processor.load(image_path)
    
    # 1. 色相和饱和度调整
    print("\n3.1 调整色相和饱和度...")
    hue_saturation = processor.copy()
    adjust_hue_saturation(hue_saturation, hue_shift=30, saturation_factor=1.5)
    hue_output = output_dir / f"{image_path.stem}_hue_saturation{image_path.suffix}"
    hue_saturation.save(hue_output)
    print(f"保存色相饱和度调整图像: {hue_output}")
    
    # 2. 色彩平衡
    print("\n3.2 应用色彩平衡...")
    color_balanced = processor.copy()
    color_balance(color_balanced, red_scale=1.1, green_scale=0.95, blue_scale=0.95)
    balance_output = output_dir / f"{image_path.stem}_color_balanced{image_path.suffix}"
    color_balanced.save(balance_output)
    print(f"保存色彩平衡图像: {balance_output}")
    
    # 3. 选择性色彩调整
    print("\n3.3 应用选择性色彩调整...")
    selective = processor.copy()
    selective_color(selective, "red", cyan=-20, magenta=0, yellow=10, black=0)
    selective_output = output_dir / f"{image_path.stem}_selective_color{image_path.suffix}"
    selective.save(selective_output)
    print(f"保存选择性色彩调整图像: {selective_output}")
    
    # 4. 灰度转换
    print("\n3.4 转换为灰度图像...")
    grayscale = processor.copy()
    convert_to_grayscale(grayscale, method="luminosity")
    grayscale_output = output_dir / f"{image_path.stem}_grayscale{image_path.suffix}"
    grayscale.save(grayscale_output)
    print(f"保存灰度图像: {grayscale_output}")
    
    # 5. 复古褐色调
    print("\n3.5 应用复古褐色调...")
    sepia = processor.copy()
    apply_sepia(sepia, intensity=0.8)
    sepia_output = output_dir / f"{image_path.stem}_sepia{image_path.suffix}"
    sepia.save(sepia_output)
    print(f"保存复古褐色调图像: {sepia_output}")
    
    print(f"\n所有色彩处理图像已保存到: {output_dir}")


def demo_custom_filters():
    """演示自定义滤镜和卷积操作"""
    print_header("4. 自定义滤镜和卷积操作")
    
    # 获取示例图像
    image_path = get_sample_image_path()
    if not image_path:
        print("错误: 未找到示例图像")
        print("请先运行: python examples/create_sample_images.py")
        return
    
    print(f"使用示例图像: {image_path.name}")
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "processed_images" / "custom_filters"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建图像处理器
    processor = ImageProcessor()
    processor.load(image_path)
    
    # 1. 锐化滤镜（自定义卷积）
    print("\n4.1 应用自定义锐化滤镜...")
    sharpen_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    sharpened = processor.copy()
    apply_custom_filter(sharpened, sharpen_kernel)
    sharpened_output = output_dir / f"{image_path.stem}_custom_sharpened{image_path.suffix}"
    sharpened.save(sharpened_output)
    print(f"保存自定义锐化图像: {sharpened_output}")
    
    # 2. 边缘检测滤镜
    print("\n4.2 应用自定义边缘检测滤镜...")
    edge_kernel = np.array([
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]
    ])
    custom_edges = processor.copy()
    apply_custom_filter(custom_edges, edge_kernel)
    edges_output = output_dir / f"{image_path.stem}_custom_edges.png"
    custom_edges.save(edges_output)
    print(f"保存自定义边缘检测图像: {edges_output}")
    
    # 3. 浮雕效果
    print("\n4.3 应用浮雕效果...")
    emboss_kernel = np.array([
        [-2, -1, 0],
        [-1, 1, 1],
        [0, 1, 2]
    ])
    embossed = processor.copy()
    apply_custom_filter(embossed, emboss_kernel)
    embossed_output = output_dir / f"{image_path.stem}_embossed.png"
    embossed.save(embossed_output)
    print(f"保存浮雕效果图像: {embossed_output}")
    
    # 4. 高斯模糊
    print("\n4.4 应用高斯模糊...")
    blurred = processor.copy()
    apply_blur(blurred, blur_type="gaussian", radius=3)
    blurred_output = output_dir / f"{image_path.stem}_gaussian_blur{image_path.suffix}"
    blurred.save(blurred_output)
    print(f"保存高斯模糊图像: {blurred_output}")
    
    # 5. 运动模糊
    print("\n4.5 应用运动模糊...")
    motion_blurred = processor.copy()
    apply_blur(motion_blurred, blur_type="motion", radius=10, angle=45)
    motion_output = output_dir / f"{image_path.stem}_motion_blur{image_path.suffix}"
    motion_blurred.save(motion_output)
    print(f"保存运动模糊图像: {motion_output}")
    
    print(f"\n所有自定义滤镜图像已保存到: {output_dir}")


def demo_transformations():
    """演示高级图像变换技术"""
    print_header("5. 高级图像变换")
    
    # 获取示例图像
    image_path = get_sample_image_path()
    if not image_path:
        print("错误: 未找到示例图像")
        print("请先运行: python examples/create_sample_images.py")
        return
    
    print(f"使用示例图像: {image_path.name}")
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "processed_images" / "transformations"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建图像处理器
    processor = ImageProcessor()
    processor.load(image_path)
    
    # 1. 旋转图像
    print("\n5.1 旋转图像...")
    rotated = processor.copy()
    rotate_image(rotated, angle=45, expand=True, fillcolor=(255, 255, 255))
    rotated_output = output_dir / f"{image_path.stem}_rotated{image_path.suffix}"
    rotated.save(rotated_output)
    print(f"保存旋转图像: {rotated_output}")
    
    # 2. 翻转图像
    print("\n5.2 翻转图像...")
    flipped = processor.copy()
    flip_image(flipped, direction="horizontal")
    flipped_output = output_dir / f"{image_path.stem}_flipped{image_path.suffix}"
    flipped.save(flipped_output)
    print(f"保存翻转图像: {flipped_output}")
    
    # 3. 透视变换
    print("\n5.3 应用透视变换...")
    # 定义透视变换的源点和目标点
    width, height = processor.width, processor.height
    src_points = [(0, 0), (width, 0), (width, height), (0, height)]
    dst_points = [(20, 50), (width-20, 10), (width-50, height-10), (10, height-50)]
    
    perspective = processor.copy()
    perspective_transform(perspective, src_points, dst_points)
    perspective_output = output_dir / f"{image_path.stem}_perspective{image_path.suffix}"
    perspective.save(perspective_output)
    print(f"保存透视变换图像: {perspective_output}")
    
    # 4. 裁剪到内容
    print("\n5.4 裁剪到内容...")
    # 先添加一些空白边框
    bordered = processor.copy()
    border_width = 20
    new_width = width + 2 * border_width
    new_height = height + 2 * border_width
    
    # 创建空白图像并粘贴原始图像
    from PIL import Image
    new_img = Image.new(processor.mode, (new_width, new_height), color=(255, 255, 255))
    new_img.paste(bordered.image, (border_width, border_width))
    bordered.image = new_img
    
    # 裁剪到内容
    cropped = bordered.copy()
    crop_to_content(cropped, tolerance=10)
    crop_output = output_dir / f"{image_path.stem}_cropped{image_path.suffix}"
    cropped.save(crop_output)
    print(f"保存裁剪图像: {crop_output}")
    
    print(f"\n所有变换图像已保存到: {output_dir}")


def demo_detection_features():
    """演示图像检测功能"""
    print_header("6. 图像检测功能")
    
    # 获取示例图像
    image_path = get_sample_image_path()
    if not image_path:
        print("错误: 未找到示例图像")
        print("请先运行: python examples/create_sample_images.py")
        return
    
    print(f"使用示例图像: {image_path.name}")
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "processed_images" / "detection"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建图像处理器
    processor = ImageProcessor()
    processor.load(image_path)
    
    try:
        # 1. 边缘检测
        print("\n6.1 检测图像边缘...")
        edges = processor.copy()
        edges_result = detect_edges(edges)
        edges_output = output_dir / f"{image_path.stem}_edges.png"
        edges.save(edges_output)
        print(f"保存边缘检测结果: {edges_output}")
        print(f"检测到的边缘信息: {edges_result}")
        
        # 2. 轮廓检测
        print("\n6.2 检测图像轮廓...")
        contours_img = processor.copy()
        contours = find_contours(contours_img, min_area=500)
        contours_output = output_dir / f"{image_path.stem}_contours.png"
        contours_img.save(contours_output)
        print(f"保存轮廓检测结果: {contours_output}")
        print(f"检测到 {len(contours)} 个轮廓")
        
        # 3. 角点检测
        print("\n6.3 检测图像角点...")
        corners_img = processor.copy()
        corners = detect_corners(corners_img, max_corners=50)
        corners_output = output_dir / f"{image_path.stem}_corners.png"
        corners_img.save(corners_output)
        print(f"保存角点检测结果: {corners_output}")
        print(f"检测到 {len(corners)} 个角点")
        
        # 4. 人脸检测（如果支持）
        print("\n6.4 尝试人脸检测...")
        try:
            face_img = processor.copy()
            faces = detect_faces(face_img)
            faces_output = output_dir / f"{image_path.stem}_faces{image_path.suffix}"
            face_img.save(faces_output)
            print(f"保存人脸检测结果: {faces_output}")
            print(f"检测到 {len(faces)} 个人脸")
        except Exception as e:
            print(f"注意: 人脸检测可能不可用或需要额外配置: {e}")
            print("跳过人脸检测演示")
            
    except Exception as e:
        print(f"检测功能演示出错: {e}")
    
    print(f"\n所有检测结果已保存到: {output_dir}")


def demo_image_restoration():
    """演示图像修复技术"""
    print_header("7. 图像修复技术")
    
    # 获取示例图像
    image_path = get_sample_image_path()
    if not image_path:
        print("错误: 未找到示例图像")
        print("请先运行: python examples/create_sample_images.py")
        return
    
    print(f"使用示例图像: {image_path.name}")
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "processed_images" / "restoration"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建图像处理器
    processor = ImageProcessor()
    processor.load(image_path)
    
    # 创建一个带有模拟噪声和缺陷的图像副本
    print("\n7.1 创建带噪声的测试图像...")
    noisy_image = processor.copy()
    
    # 添加一些高斯噪声（模拟）
    # 注意：这里使用PIL的Image.effect_noise方法作为示例
    from PIL import Image, ImageDraw
    width, height = noisy_image.width, noisy_image.height
    
    # 转换为numpy数组进行操作
    import numpy as np
    img_array = np.array(noisy_image.image)
    
    # 添加高斯噪声
    mean = 0
    std = 20
    gaussian_noise = np.random.normal(mean, std, img_array.shape)
    noisy_array = img_array + gaussian_noise
    noisy_array = np.clip(noisy_array, 0, 255).astype(np.uint8)
    
    # 转换回PIL图像
    noisy_image.image = Image.fromarray(noisy_array)
    
    # 添加一些模拟划痕
    draw = ImageDraw.Draw(noisy_image.image)
    for _ in range(5):
        x1 = np.random.randint(0, width)
        y1 = np.random.randint(0, height)
        x2 = np.random.randint(0, width)
        y2 = np.random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255), width=1)
    
    noisy_output = output_dir / f"{image_path.stem}_noisy{image_path.suffix}"
    noisy_image.save(noisy_output)
    print(f"保存带噪声的图像: {noisy_output}")
    
    # 应用降噪
    print("\n7.2 应用降噪修复...")
    denoised = noisy_image.copy()
    smart_denoise(denoised, strength=0.7)
    denoised_output = output_dir / f"{image_path.stem}_denoised_restored{image_path.suffix}"
    denoised.save(denoised_output)
    print(f"保存降噪修复图像: {denoised_output}")
    
    # 应用锐化来恢复细节
    print("\n7.3 应用锐化恢复细节...")
    restored = denoised.copy()
    apply_sharpen(restored, amount=1.2, radius=1.0)
    restored_output = output_dir / f"{image_path.stem}_fully_restored{image_path.suffix}"
    restored.save(restored_output)
    print(f"保存完全修复图像: {restored_output}")
    
    print(f"\n所有修复图像已保存到: {output_dir}")
    print("\n图像修复步骤:")
    print("1. 创建带噪声和划痕的测试图像")
    print("2. 应用智能降噪去除高斯噪声")
    print("3. 应用锐化增强恢复图像细节")


def main():
    """主函数"""
    print_header("Gneiss-Engine 高级图像处理示例")
    
    try:
        # 运行各个演示
        demo_image_enhancement()
        demo_edge_detection_and_segmentation()
        demo_advanced_color_processing()
        demo_custom_filters()
        demo_transformations()
        demo_detection_features()
        demo_image_restoration()
        
        print("\n" + "=" * 70)
        print("所有高级图像处理演示已完成！")
        print("您可以在 processed_images 目录下的各个子目录中查看处理结果。")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n感谢使用 Gneiss-Engine!")


if __name__ == "__main__":
    main()
