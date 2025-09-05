# Gneiss-Engine 本地开发环境设置指南

本指南将帮助您配置Gneiss-Engine的本地开发环境。

## 系统要求

- Python 3.7 或更高版本
- pip（Python包管理器）
- git（版本控制系统）

## 本地开发安装步骤

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/gneiss-engine.git
cd gneiss-engine
```

2. 安装基础依赖：

```bash
pip install -r requirements.txt
```

3. 以开发模式安装：

```bash
pip install -e .
```

这将以"可编辑"模式安装包，允许您修改代码并立即看到变化。

## 安装开发依赖

如需运行测试或进行开发，可安装额外依赖：

```bash
pip install -r requirements-dev.txt
```

## 验证安装

安装完成后，您可以通过运行以下Python代码来验证安装是否成功：

```python
from gneiss import Image
print("Gneiss-Engine 开发环境已成功设置！")
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

## 更新代码

要获取最新的代码更改，请运行：

```bash
git pull origin main
```

然后重新安装：

```bash
pip install -e .
```

## 卸载开发环境

如果需要卸载开发环境中的Gneiss-Engine，请运行：

```bash
pip uninstall gneiss-engine