# Gneiss-Engine 🪨 - 中文文档

[![构建状态](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yourusername/gneiss-engine)
[![PyPI 版本](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/gneiss-engine/)
[![许可证: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个坚固、高性能的Python核心，用于图像变形处理。

## 项目简介

在软件开发中，处理基本的图像任务（如批量转换、智能重命名或优化）常常需要使用多个库，显得分散而繁琐。Gneiss-Engine旨在通过为所有常见图像处理需求提供单一、强大且可靠的核心来解决这个问题。

名称"Gneiss"（发音为/naɪs/，像"nice"）的灵感来自变质岩，它是在巨大的热量和压力下由现有岩石转化形成的。同样，Gneiss-Engine被设计为一个基础工具包，可以重塑和重组您的图像资源，为所有图像处理任务提供坚实的分层基础。

⚠️ **重要说明**: 个人开发者的早期实验项目

Gneiss-Engine 目前是**个人开发者**在业余时间进行的**实验性项目**，处于**非常早期的开发阶段**。这意味着：

1. 这是一个**个人项目**，没有公司或团队支持
2. 开发进度**完全取决于个人时间安排**，可能非常缓慢
3. 核心功能和API**随时可能发生重大变化**
4. **不建议**在生产环境中使用当前版本
5. 项目**可能长期停留在实验阶段**，不保证会持续维护

虽然我会尽力完善这个项目，但请理解作为个人开发者，时间和资源都有限。您的理解和包容非常重要！

我们欢迎想法、反馈和未来的贡献者来帮助塑造它的方向。

## ✨ 核心特性（愿景）

Gneiss-Engine设计时考虑了以下关键功能：

🔄 **变形转换**: 简单而强大的API，用于在各种格式（如PNG、JPEG、WEBP、AVIF）之间转换图像，类似于岩石改变其基本结构。

✍️ **智能重命名**: 基于自定义模式、顺序编号甚至图像元数据（如EXIF数据）的高级批量重命名功能。

🔍 **高质量调整大小**: 易于使用的函数，用于缩放图像同时保持宽高比和图像质量。

💧 **水印**: 流畅的界面，用于添加文本或基于图像的水印，可控制不透明度、位置和平铺。

🛠️ **元数据管理**: 轻松读取、写入和剥离图像元数据（EXIF、IPTC等）的能力。

⚡ **性能优先**: 构建在高度优化的库（如Pillow-SIMD）之上，确保速度是主要特性。

## 🚀 我们的理念

**简单第一**: 我们相信强大的工具不必复杂。Gneiss-Engine将具有干净、可链接且高度可读的API。

**可扩展性**: 设计为核心"引擎"，可以轻松扩展自定义插件和功能。

**可靠性**: 专注于全面的测试和可预测的行为。它应该是您图像处理流程的基石。

## 安装

### 用户安装 (发布后可用)
```bash
pip install gneiss-engine
```

### 开发者安装 (当前本地安装方式)
1. 克隆仓库:
```bash
git clone https://github.com/yourusername/gneiss-engine.git
cd gneiss-engine
```

2. 以开发模式安装:
```bash
pip install -e .
```

这将以"可编辑"模式安装包，允许您修改代码并立即看到变化。

## 使用示例

```python
from gneiss import Image

# 简单、流畅的API，用于可链接操作
try:
    Image("path/to/source_image.jpg")
        .resize(width=1024)
        .add_watermark("logo.png", position="bottom_right", opacity=0.7)
        .to_format("webp", quality=90)
        .save("path/to/output/new_image.webp")
    
    print("图像处理成功！")

except Exception as e:
    print(f"发生错误: {e}")
```

## 文档

- [安装指南](docs/installation.md)
- [使用指南](docs/usage_guide.md)

## 如何贡献

我们目前尚未接受功能性的pull request，但我们非常欢迎想法和讨论！如果您有建议，在我们的早期代码中发现错误，或想成为项目未来的一部分，请在GitHub上创建一个issue。

您在这个关键初始阶段的反馈非常宝贵。

## 许可证

根据MIT许可证分发。有关更多信息，请参阅`LICENSE`文件。

## 英文文档

[查看英文README](README.md)