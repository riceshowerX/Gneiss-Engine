
# Gneiss-Engine

[![Build Status](https://github.com/yourusername/Gneiss-Engine/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/Gneiss-Engine/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/gneiss-engine.svg)](https://pypi.org/project/gneiss-engine/)

**Gneiss-Engine** 是一个强大、灵活且高效的 Python 图像处理库，提供流畅的 API 和高级功能，帮助开发者轻松完成各种图像处理任务。

## 主要特性

### 🚀 核心功能
- **流畅的链式 API** - 支持方法链式调用，提高代码可读性和简洁性
- **批量图像处理** - 并行处理大量图像，支持多种操作
- **多格式支持** - 支持常见格式以及高级格式（AVIF、HEIC，需安装额外依赖）
- **元数据管理** - 完整的元数据读取、修改和清除功能
- **高级文件操作工具** - 强大的文件查找、移动、重命名和管理功能

### ✨ 图像处理能力
- **基本变换**：缩放、裁剪、旋转、翻转
- **高级变换**：透视变换、亮度对比度调整、自适应亮度
- **滤镜效果**：模糊、锐化、灰度转换、色彩调整
- **缩略图生成** - 高效创建保持纵横比的缩略图
- **水印添加** - 支持多种水印位置和透明度设置

### 🔧 性能优化
- **资源感知** - 根据系统资源动态调整并行处理能力
- **Pillow-SIMD 优化** - 在支持的平台上使用 SIMD 指令加速
- **错误恢复机制** - 支持跳过现有文件、错误限制等高级处理选项
- **进度跟踪** - 详细的处理进度和结果报告

### 📊 高级功能
- **直方图分析** - 用于自适应图像处理
- **精确的错误报告** - 详细的错误信息和处理摘要
- **处理统计** - 提供成功率、错误率等处理指标
- **自定义工作流** - 支持创建和执行自定义图像处理管道
- **格式转换统计** - 提供文件大小变化等关键指标

### 🛠 实用工具
- **示例图像生成** - 内置工具快速创建测试图像
- **文件批量操作** - 高效重命名、移动、删除和筛选文件
- **文件格式分析** - 按扩展名分组和分析文件

## 安装

### 基本安装
```bash
pip install gneiss-engine
```

### 安装所有可选依赖
```bash
pip install gneiss-engine[all]
```

### 安装特定格式支持
```bash
# AVIF 格式支持
pip install gneiss-engine[avif]

# HEIC 格式支持
pip install gneiss-engine[heic]
```

## 快速开始

### 基本图像处理

```python
from gneiss.core import Image

# 打开图像
img = Image.open('example.jpg')

# 缩放并保存
img.resize(width=800, height=600, maintain_aspect=True).save('resized.jpg')

# 应用多个操作并保存为不同格式
img.rotate(90)
   .crop(left=10, top=10, right=500, bottom=500)
   .convert_to_grayscale()
   .save('processed.png')

# 创建缩略图
img.thumbnail(size=(128, 128), resample='LANCZOS')
img.save('thumbnail.jpg')
```

### 批量处理

```python
from gneiss.core import BatchProcessor
import os
from pathlib import Path

# 创建处理器
processor = BatchProcessor()

# 获取目录中所有图片
image_dir = 'images/'
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) 
               if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# 批量转换格式
results = processor.convert_format(
    image_paths=image_paths,
    output_format='webp',
    output_dir='converted/',
    quality=80,
    show_progress=True,
    skip_existing=True,
    stop_on_error=False
)

# 打印处理结果统计
print(f"处理总览:")
print(f"总文件数: {results['metadata']['total']}")
print(f"成功数: {results['metadata']['success']}")
print(f"失败数: {results['metadata']['failed']}")
print(f"跳过数: {results['metadata']['skipped']}")

# 批量调整大小
results = processor.resize_images(
    image_paths=image_paths,
    width=1024,
    maintain_aspect=True,
    output_dir='resized/',
    output_suffix='_resized'
)
```

### 文件操作工具使用

```python
from gneiss.utils.file_utils import (
    find_images,
    ensure_directory_exists,
    get_unique_filename,
    group_files_by_extension,
    get_file_size,
    move_files_with_progress
)

# 查找图像文件
images = find_images('path/to/directory', recursive=True, extensions=['.jpg', '.png'])
print(f"找到 {len(images)} 张图像")

# 确保目录存在
output_dir = 'path/to/output'
ensure_directory_exists(output_dir)

# 获取唯一文件名以避免覆盖
output_path = get_unique_filename('path/to/output/image.jpg')

# 按扩展名分组文件
all_files = ['file1.jpg', 'file2.png', 'file3.txt']
grouped = group_files_by_extension(all_files)
print(f"JPG文件数量: {len(grouped.get('.jpg', []))}")

# 获取文件大小（人类可读格式）
size = get_file_size('path/to/image.jpg', human_readable=True)
print(f"文件大小: {size}")

# 移动文件（带进度跟踪）
files_to_move = ['file1.jpg', 'file2.png']
dest_dir = 'path/to/destination'
results = move_files_with_progress(files_to_move, dest_dir)

# 生成示例图像（用于测试）
# python examples/create_sample_images.py
# 然后使用批量处理功能处理这些图像
# python examples/batch_processing.py
```

## 功能详情

### 文件工具类 `file_utils`

**图像查找:**
- `find_images(directory, recursive=False, extensions=None)` - 查找指定目录中的图像文件
- `get_files_by_extension(directory, extensions, recursive=False)` - 按扩展名获取文件

**文件管理:**
- `ensure_directory_exists(directory)` - 确保目录存在，如果不存在则创建
- `get_unique_filename(file_path)` - 获取唯一文件名，避免覆盖
- `generate_output_filename(input_file, output_dir, suffix='', extension=None)` - 生成输出文件名

**批量操作:**
- `batch_rename(files, pattern, replacement, use_regex=False)` - 批量重命名文件
- `apply_rename(rename_map)` - 应用重命名映射
- `move_files_with_progress(files, destination)` - 移动文件并显示进度
- `remove_files_with_progress(files)` - 删除文件并显示进度

**文件分析:**
- `group_files_by_extension(files)` - 按扩展名分组文件
- `get_file_size(file_path, human_readable=False)` - 获取文件大小
- `filter_files_by_pattern(files, pattern, use_regex=False)` - 按模式筛选文件
- `generate_sequential_names(directory, base_name, extension, start_number=1, padding=3)` - 生成顺序文件名

### 图像处理核心类 `Image`

**打开和保存图像:**
- `Image.open(path)` - 从文件打开图像
- `Image.from_bytes(bytes_data)` - 从字节数据创建图像
- `img.save(path, format=None, quality=None, optimize=True)` - 保存图像

**基本变换:**
- `img.resize(width=None, height=None, maintain_aspect=True, resample='LANCZOS')` - 调整图像大小
- `img.rotate(angle, expand=False, fillcolor=None)` - 旋转图像
- `img.crop(left, top, right, bottom)` - 裁剪图像
- `img.flip(horizontal=False, vertical=False)` - 翻转图像

**高级变换:**
- `img.thumbnail(size, resample='LANCZOS')` - 创建缩略图
- `img.perspective_transform(data)` - 应用透视变换
- `img.adaptive_brightness(threshold=0.5, factor=1.2)` - 自适应亮度调整

**效果和滤镜:**
- `img.convert_to_grayscale()` - 转换为灰度图像
- `img.blur(radius=2)` - 应用模糊效果
- `img.sharpen(factor=2.0)` - 锐化图像
- `img.adjust_brightness(factor=1.0)` - 调整亮度
- `img.adjust_contrast(factor=1.0)` - 调整对比度

**水印和元数据:**
- `img.add_watermark(watermark_path, position='bottom_right', opacity=0.5)` - 添加水印
- `img.strip_metadata()` - 清除所有元数据
- `img.get_metadata()` - 获取图像元数据

### 批量处理类 `BatchProcessor`

**配置:**
- `BatchProcessor(max_workers=None, error_limit=None)` - 创建批处理器

**批量操作:**
- `processor.process_images(image_paths, operation, output_dir=None, ...)` - 通用批处理方法
- `processor.convert_format(image_paths, output_format, output_dir=None, ...)` - 批量转换格式
- `processor.resize_images(image_paths, width=None, height=None, ...)` - 批量调整大小
- `processor.add_watermarks(image_paths, watermark_path, ...)` - 批量添加水印
- `processor.strip_metadata(image_paths, ...)` - 批量清除元数据

**高级参数:**
- `show_progress` - 是否显示进度条
- `skip_existing` - 是否跳过已存在的输出文件
- `stop_on_error` - 是否在遇到错误时停止处理
- `output_suffix` - 添加到输出文件名的后缀
- `error_limit` - 处理停止前允许的最大错误数

### 示例脚本

Gneiss-Engine 提供了一系列示例脚本来演示库的使用:

1. **创建示例图像** - 生成测试用的图像集合
   ```bash
   python examples/create_sample_images.py
   ```

2. **批量处理示例** - 演示各种批量图像处理操作
   ```bash
   python examples/batch_processing.py
   ```

3. **文件操作示例** - 演示文件管理和批处理功能
   ```bash
   python examples/file_operations.py
   ```

4. **高级图像处理示例** - 演示高级图像处理技术，包括图像增强、边缘检测、分割等
   ```bash
   python examples/advanced_image_processing.py
   ```

5. **示例文档** - 详细了解所有示例脚本的功能和用法
   ```bash
   cat examples/README.md
   ```

### 高级配置

### 系统资源优化

BatchProcessor 会自动检测系统资源并优化工作线程数量。您也可以手动指定：

```python
from gneiss.core import BatchProcessor

# 限制最大工作线程数
processor = BatchProcessor(max_workers=4)
```

### 格式支持配置

对于高级格式支持（AVIF、HEIC），需要安装相应的依赖：

```bash
# AVIF 支持
pip install pillow-avif>=1.0.0

# HEIC 支持
pip install pillow-heif>=0.10.0
```

## 错误处理和故障排除

### 批量处理错误策略

```python
# 设置错误限制并跳过存在的文件
results = processor.process_images(
    image_paths=image_paths,
    operation=my_operation,
    output_dir='output/',
    skip_existing=True,
    stop_on_error=False,
    error_limit=5  # 最多容忍5个错误
)

# 查看失败的文件
for path, result in results.items():
    if isinstance(result, Exception):
        print(f"处理失败: {path}, 错误: {result}")
```

### 常见问题解决方案

- **内存不足**: 减少批量处理的图像数量或降低工作线程数
- **格式支持问题**: 确保已安装相应的格式依赖包
- **水印透明度**: 对于某些格式，可能需要在保存时设置 `quality` 参数以保留透明度

## 开发和贡献

### 安装开发环境

```bash
# 克隆仓库
git clone https://github.com/yourusername/Gneiss-Engine.git
cd Gneiss-Engine

# 安装开发依赖
pip install -e "[dev]"

# 运行测试
pytest
```

### 代码规范

项目使用以下工具进行代码质量控制：
- **Black**: 代码格式化
- **isort**: 导入语句排序
- **flake8**: 代码质量检查
- **mypy**: 类型检查

### 运行示例

```bash
# 生成示例图像
python examples/create_sample_images.py

# 运行文件操作示例
python examples/file_operations.py

# 运行批量处理示例
python examples/batch_processing.py

# 运行高级图像处理示例
python examples/advanced_image_processing.py

# 运行所有测试
python -m unittest discover tests

## 许可证

Distributed under the MIT License. See `LICENSE` file for more information.