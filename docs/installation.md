# Gneiss-Engine 安装指南

本指南将帮助您在不同环境中安装Gneiss-Engine。

## 系统要求

- Python 3.7 或更高版本
- pip（Python包管理器）

## 基本安装

使用pip安装Gneiss-Engine的最新稳定版本：

```bash
pip install gneiss-engine
```

## 从源代码安装

如果您想从源代码安装Gneiss-Engine，可以按照以下步骤操作：

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/gneiss-engine.git
cd gneiss-engine
```

2. 安装依赖项：

```bash
pip install -r requirements.txt
```

3. 安装Gneiss-Engine：

```bash
pip install -e .
```

这将以开发模式安装Gneiss-Engine，这意味着您对源代码的任何更改都会立即反映在安装中。

## 安装可选依赖

Gneiss-Engine有一些可选依赖项，可以提供额外的功能：

```bash
# 安装开发依赖（用于测试和开发）
pip install gneiss-engine[dev]
```

## 验证安装

安装完成后，您可以通过运行以下Python代码来验证安装是否成功：

```python
from gneiss import Image
print(f"Gneiss-Engine 已成功安装！版本: {Image.__version__}")
```

## 常见问题

### Pillow安装问题

Gneiss-Engine依赖于Pillow库进行图像处理。如果您在安装Pillow时遇到问题，可能需要安装一些系统依赖项：

#### Ubuntu/Debian：

```bash
sudo apt-get update
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev
```

#### macOS：

```bash
brew install libtiff libjpeg webp little-cms2
```

#### Windows：

在Windows上，Pillow通常可以通过pip直接安装，无需额外的系统依赖项。

### 其他问题

如果您遇到其他安装问题，请查看[GitHub仓库的问题页面](https://github.com/yourusername/gneiss-engine/issues)，或者提交一个新的问题。

## 升级

要升级到最新版本的Gneiss-Engine，请运行：

```bash
pip install --upgrade gneiss-engine
```

## 卸载

如果需要卸载Gneiss-Engine，请运行：

```bash
pip uninstall gneiss-engine