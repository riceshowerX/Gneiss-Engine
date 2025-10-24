#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
生成示例图像脚本

此脚本用于为 Gneiss-Engine 示例程序生成测试用图像文件。
它会在 sample_images 目录中创建几个不同类型的示例图像，
专门设计用于演示各种图像处理功能。
"""

import os
import sys
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


def create_basic_sample_image(path, width, height, color, text=None):
    """
    创建基本的示例图像（保持向后兼容）
    
    Args:
        path: 输出文件路径
        width: 图像宽度
        height: 图像高度
        color: RGB 颜色元组
        text: 可选的文本内容
    """
    # 创建新图像
    img = Image.new("RGB", (width, height), color)

    # 添加文本（如果提供）
    if text:
        draw = ImageDraw.Draw(img)

        # 尝试使用可能可用的字体
        try:
            # 尝试使用 Arial，Windows 上常见
            font = ImageFont.truetype("arial.ttf", size=36)
        except IOError:
            # 回退到默认字体
            font = ImageFont.load_default()

        # 计算文本位置以使其居中
        # 在较新的 Pillow 版本中，使用 getbbox() 而不是 getsize() 或 textsize()
        try:
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # 为较旧的 Pillow 版本回退
            try:
                text_width, text_height = draw.textsize(text, font=font)
            except AttributeError:
                # 非常旧的 Pillow 版本
                text_width, text_height = (
                    font.getsize(text)
                    if hasattr(font, "getsize")
                    else (width // 2, height // 2)
                )

        position = ((width - text_width) // 2, (height - text_height) // 2)

        # 绘制文本
        draw.text(position, text, fill=(255, 255, 255), font=font)

    # 保存图像
    img.save(path)
    print(f"创建基本示例图像: {path}")


def create_perspective_sample(path):
    """
    创建用于透视变换测试的图像
    
    Args:
        path: 输出文件路径
    """
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    # 绘制一些图形和文本
    # 主矩形
    draw.rectangle([100, 100, 700, 500], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    
    # 中心文本
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype('arial.ttf', 40)
    except IOError:
        # 如果找不到字体，使用默认字体
        font = ImageFont.load_default()
    
    text = "透视变换测试"
    
    # 计算文本尺寸
    try:
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        try:
            text_width, text_height = draw.textsize(text, font=font)
        except AttributeError:
            text_width, text_height = (width // 2, height // 2)
    
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
    
    # 添加一些细节
    draw.line([100, 100, 700, 500], fill=(200, 0, 0), width=2)
    draw.line([700, 100, 100, 500], fill=(200, 0, 0), width=2)
    
    # 保存图像
    img.save(path, 'JPEG', quality=95)
    print(f"创建透视变换测试图像: {path}")


def create_low_light_sample(path):
    """
    创建用于亮度调整测试的低光照图像
    
    Args:
        path: 输出文件路径
    """
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # 创建渐变背景
    for y in range(0, height, 5):  # 为了效率，减少循环次数
        for x in range(0, width, 5):
            # 创建从暗到亮的渐变
            brightness = int((y / height) * 100)
            # 填充5x5的块而不是单个像素
            draw.rectangle([x, y, x+5, y+5], fill=(brightness, brightness, brightness + 20))
    
    # 添加一些"暗区域"文本
    try:
        font = ImageFont.truetype('arial.ttf', 36)
    except IOError:
        font = ImageFont.load_default()
    
    text = "低光照区域测试"
    
    # 计算文本尺寸
    try:
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        try:
            text_width, text_height = draw.textsize(text, font=font)
        except AttributeError:
            text_width, text_height = (width // 2, height // 2)
    
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    # 使用较亮但仍不太明显的颜色
    draw.text((text_x, text_y), text, fill=(100, 100, 100), font=font)
    
    # 添加一些小亮点
    for i in range(20):
        x = int((hash(str(i)) % 100) / 100 * width)
        y = int((hash(str(i+1)) % 100) / 100 * height)
        size = (hash(str(i+2)) % 5) + 1
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 255))
    
    # 降低整体亮度
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.4)
    
    # 保存图像
    img.save(path, 'JPEG', quality=95)
    print(f"创建低光照测试图像: {path}")


def create_texture_sample(path):
    """
    创建用于滤镜效果测试的纹理图像
    
    Args:
        path: 输出文件路径
    """
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 创建棋盘格背景
    cell_size = 40
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            if (x // cell_size + y // cell_size) % 2 == 0:
                draw.rectangle([x, y, x+cell_size, y+cell_size], fill=(240, 240, 240))
    
    # 添加一些圆形
    for i in range(5):
        x = 200 + i * 100
        y = 300
        radius = 30 + i * 10
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                     fill=(50 + i*40, 100 + i*20, 200 - i*30))
    
    # 添加一些文本
    try:
        font = ImageFont.truetype('arial.ttf', 28)
    except IOError:
        font = ImageFont.load_default()
    
    draw.text((300, 100), "滤镜效果测试", fill=(0, 0, 0), font=font)
    draw.text((300, 500), "锐化和模糊测试区域", fill=(0, 0, 0), font=font)
    
    # 添加一些细线
    for i in range(10):
        y = 200 + i * 10
        draw.line([100, y, 700, y], fill=(150, 150, 150), width=1)
    
    # 保存图像
    img.save(path, 'JPEG', quality=95)
    print(f"创建纹理测试图像: {path}")


def create_logo_sample(path):
    """
    创建用于缩略图测试的图像（PNG格式，带透明背景）
    
    Args:
        path: 输出文件路径
    """
    width, height = 512, 512
    # 创建带透明通道的图像
    img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制一个圆形背景
    radius = 200
    draw.ellipse([width//2 - radius, height//2 - radius, 
                  width//2 + radius, height//2 + radius], 
                 fill=(0, 120, 215, 255))
    
    # 添加白色文字
    try:
        font = ImageFont.truetype('arial.ttf', 60)
    except IOError:
        font = ImageFont.load_default()
    
    text = "GNEISS"
    
    # 计算文本尺寸
    try:
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        try:
            text_width, text_height = draw.textsize(text, font=font)
        except AttributeError:
            text_width, text_height = (width // 2, height // 2)
    
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    
    # 添加较小的子文本
    try:
        small_font = ImageFont.truetype('arial.ttf', 30)
    except IOError:
        small_font = ImageFont.load_default()
    
    sub_text = "ENGINE"
    
    # 计算子文本尺寸
    try:
        sub_bbox = small_font.getbbox(sub_text)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_height = sub_bbox[3] - sub_bbox[1]
    except AttributeError:
        try:
            sub_width, sub_height = draw.textsize(sub_text, font=small_font)
        except AttributeError:
            sub_width, sub_height = (width // 3, height // 3)
    
    sub_x = (width - sub_width) // 2
    sub_y = text_y + text_height + 20
    draw.text((sub_x, sub_y), sub_text, fill=(255, 255, 255), font=small_font)
    
    # 添加一些装饰元素
    for i in range(8):
        angle = (360 / 8) * i
        # 简单的角度计算
        rad = math.radians(angle)
        outer_x = width // 2 + int(math.cos(rad) * (radius + 40))
        outer_y = height // 2 + int(math.sin(rad) * (radius + 40))
        inner_x = width // 2 + int(math.cos(rad) * radius)
        inner_y = height // 2 + int(math.sin(rad) * radius)
        draw.line([inner_x, inner_y, outer_x, outer_y], fill=(255, 255, 255, 180), width=3)
    
    # 保存为PNG格式以保留透明度
    img.save(path, 'PNG')
    print(f"创建PNG标志测试图像: {path}")


def create_metadata_sample(path):
    """
    创建用于元数据测试的图像
    
    Args:
        path: 输出文件路径
    """
    width, height = 600, 400
    img = Image.new('RGB', (width, height), color=(220, 230, 240))
    draw = ImageDraw.Draw(img)
    
    # 绘制一个简单的场景
    # 太阳
    draw.ellipse([450, 50, 550, 150], fill=(255, 240, 0))
    
    # 山
    draw.polygon([0, 300, 300, 100, 600, 300], fill=(50, 150, 50))
    
    # 湖水
    draw.rectangle([0, 300, 600, 400], fill=(100, 200, 255))
    
    # 添加标题
    try:
        font = ImageFont.truetype('arial.ttf', 32)
    except IOError:
        font = ImageFont.load_default()
    
    draw.text((150, 150), "元数据测试图像", fill=(0, 0, 0), font=font)
    
    # 保存图像
    img.save(path, 'PNG')
    print(f"创建元数据测试图像: {path}")


def main():
    """
    主函数，创建所有示例图像
    """
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 创建示例图像目录
    sample_dir = Path(script_dir) / "sample_images"
    sample_dir.mkdir(parents=True, exist_ok=True)

    print("开始生成示例图像...")
    
    try:
        # 生成专门的功能测试图像
        create_perspective_sample(sample_dir / "sample1.jpg")
        create_low_light_sample(sample_dir / "sample2.jpg")
        create_texture_sample(sample_dir / "sample3.jpg")
        create_logo_sample(sample_dir / "sample4.png")
        create_metadata_sample(sample_dir / "sample5.png")

        print(f"\n成功创建5个示例图像在 {sample_dir} 目录中")
        print("\n您现在可以运行其他示例脚本，例如:")
        print("  python advanced_features.py")
        print("  python batch_processing.py")
        
    except Exception as e:
        print(f"\n生成示例图像时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
