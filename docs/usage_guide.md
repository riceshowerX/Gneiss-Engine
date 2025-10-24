# Gneiss-Engine 使用指南

Gneiss-Engine是一个强大的Python图像处理库，提供了简单而流畅的API来执行各种图像操作。本指南将帮助您开始使用Gneiss-Engine的核心功能。

## 安装

使用pip安装Gneiss-Engine：

```bash
pip install gneiss-engine
```

## 基本用法

### 导入库

```python
from gneiss import Image
```

### 加载图像

```python
# 从文件路径加载图像
img = Image("path/to/your/image.jpg")

# 或者从PIL Image对象加载
from PIL import Image as PILImage
pil_img = PILImage.open("path/to/your/image.jpg")
img = Image(pil_img)
```

### 调整图像大小

```python
# 指定宽度，保持纵横比
resized_img = img.resize(width=800)

# 指定高度，保持纵横比
resized_img = img.resize(height=600)

# 指定宽度和高度，保持纵横比（将适应指定的尺寸）
resized_img = img.resize(width=800, height=600)

# 指定宽度和高度，不保持纵横比
resized_img = img.resize(width=800, height=600, maintain_aspect=False)
```

### 裁剪图像

```python
# 裁剪图像（左、上、右、下坐标）
cropped_img = img.crop(100, 100, 500, 400)
```

### 添加水印

```python
# 添加图像水印
watermarked_img = img.add_watermark(
    watermark="path/to/watermark.png",
    position="bottom_right",  # 选项: "center", "top_left", "top_right", "bottom_left", "bottom_right"
    opacity=0.7,
    padding=10
)

# 添加文本水印
text_watermarked_img = img.add_text_watermark(
    text="© 2025 Your Name",
    position="bottom_right",
    font_size=24,
    color=(255, 255, 255, 180)  # RGBA颜色（白色，70%不透明度）
)
```

### 调整图像属性

```python
# 调整亮度（>1.0增加亮度，<1.0降低亮度）
brightened_img = img.adjust_brightness(1.2)

# 调整对比度（>1.0增加对比度，<1.0降低对比度）
contrasted_img = img.adjust_contrast(1.3)

# 调整颜色饱和度（>1.0增加饱和度，<1.0降低饱和度，0.0为灰度）
saturated_img = img.adjust_color(1.5)

# 调整锐度（>1.0增加锐度，<1.0降低锐度）
sharpened_img = img.adjust_sharpness(1.4)

# 转换为灰度
grayscale_img = img.grayscale()
```

### 旋转和翻转

```python
# 旋转图像（角度，逆时针）
rotated_img = img.rotate(90)

# 水平翻转
flipped_h_img = img.flip(horizontal=True)

# 垂直翻转
flipped_v_img = img.flip(vertical=True)

# 同时水平和垂直翻转
flipped_both_img = img.flip(horizontal=True, vertical=True)
```

### 转换格式和保存

```python
# 转换为WEBP格式并保存
img.to_format("WEBP", quality=90).save("output/image.webp")

# 转换为JPEG格式并保存
img.to_format("JPEG", quality=85).save("output/image.jpg")

# 转换为PNG格式并保存
img.to_format("PNG").save("output/image.png")
```

### 链式操作

Gneiss-Engine的一个强大特性是能够链式调用方法，以简洁的方式执行复杂的操作序列：

```python
# 链式操作示例
img.resize(width=1200) \
   .adjust_brightness(1.1) \
   .adjust_contrast(1.2) \
   .add_text_watermark(
       text="© 2025 Your Name",
       position="bottom_right",
       font_size=18,
       color=(255, 255, 255, 180)
   ) \
   .to_format("WEBP", quality=90) \
   .save("output/processed_image.webp")
```

## 批处理

Gneiss-Engine提供了强大的批处理功能，支持并行处理以优化性能：

**性能优化建议**：
- 使用 `BatchProcessor(max_workers=4)` 调整并行线程数以匹配您的 CPU 核心数。
- 对于大规模批处理，建议先测试小批量数据以验证性能。

```python
from gneiss.core.batch import BatchProcessor

# 创建批处理器
batch_processor = BatchProcessor()

# 获取要处理的图像路径列表
image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]

# 批量调整大小
results = batch_processor.resize_images(
    image_paths=image_paths,
    width=800,
    maintain_aspect=True,
    output_dir="output/resized",
    show_progress=True
)

# 批量转换格式
results = batch_processor.convert_format(
    image_paths=image_paths,
    output_format="WEBP",
    output_dir="output/webp",
    quality=90,
    show_progress=True
)

# 批量添加水印
results = batch_processor.add_text_watermark_to_images(
    image_paths=image_paths,
    text="© 2025 Your Name",
    position="bottom_right",
    font_size=24,
    color=(255, 255, 255, 180),
    output_dir="output/watermarked",
    show_progress=True
)

# 自定义批处理操作
def custom_operation(img):
    return img.resize(width=1200) \
              .adjust_brightness(1.1) \
              .adjust_contrast(1.2) \
              .add_text_watermark(
                  text="© 2025 Your Name",
                  position="bottom_right",
                  font_size=18,
                  color=(255, 255, 255, 180)
              )

results = batch_processor.process_images(
    image_paths=image_paths,
    operation=custom_operation,
    output_dir="output/custom",
    output_format="JPEG",
    show_progress=True
)
```

## 文件操作

Gneiss-Engine提供了一些实用工具来处理文件操作：

```python
from gneiss.utils.file_utils import (
    get_files_by_extension,
    batch_rename,
    apply_rename,
    generate_sequential_names
)

# 获取指定扩展名的文件
image_files = get_files_by_extension(
    "path/to/directory",
    extensions=['.jpg', '.png'],
    recursive=True
)

# 批量重命名（生成重命名映射）
rename_map = batch_rename(
    files=image_files,
    pattern="IMG_",
    replacement="vacation_",
    use_regex=False
)

# 应用重命名
results = apply_rename(rename_map)

# 生成序列文件名
sequential_names = generate_sequential_names(
    directory="path/to/directory",
    base_name="photo_",
    extension="jpg",
    start_number=1,
    padding=3
)
```

## 元数据操作

Gneiss-Engine可以处理图像元数据，包括读取、写入和剥离：

**剥离元数据**：
```python
# 剥离所有元数据
stripped_img = img.strip_metadata()
stripped_img.save("output/no_metadata.jpg")
```

**注意**：剥离元数据适用于隐私保护或合规性要求。

```python
from gneiss.utils.metadata_utils import (
    extract_exif,
    get_image_metadata,
    get_creation_date,
    get_gps_coordinates,
    strip_all_metadata,
    copy_metadata
)

# 提取EXIF数据
exif_data = extract_exif("path/to/image.jpg")

# 获取全面的元数据
metadata = get_image_metadata("path/to/image.jpg")

# 获取创建日期
creation_date = get_creation_date("path/to/image.jpg")

# 获取GPS坐标
gps_coords = get_gps_coordinates("path/to/image.jpg")

# 去除所有元数据
strip_all_metadata("path/to/image.jpg", "path/to/output.jpg")

# 复制元数据
copy_metadata("source.jpg", "target.jpg")
```

## 错误处理

Gneiss-Engine使用Python的异常处理机制。建议在使用库时使用try-except块：

```python
try:
    img = Image("path/to/image.jpg")
    processed_img = img.resize(width=800) \
                       .add_text_watermark("© 2025") \
                       .to_format("WEBP")
    processed_img.save("output/processed.webp")
    print("图像处理成功！")
except FileNotFoundError:
    print("找不到图像文件")
except ValueError as e:
    print(f"处理图像时出错: {e}")
except Exception as e:
    print(f"发生未预期的错误: {e}")
```

## 高级用法

有关更高级的用法和示例，请参阅`examples`目录中的示例脚本：

- `examples/basic_usage.py` - 基本用法示例
- `examples/batch_processing.py` - 批处理示例
- `examples/file_operations.py` - 文件操作示例
- `examples/metadata_operations.py` - 元数据操作示例