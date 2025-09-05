# 贡献指南

感谢您考虑为Gneiss-Engine做出贡献！作为一个个人爱好项目，我们非常欢迎社区的参与和支持。

## 项目状态

请注意，Gneiss-Engine目前处于早期开发阶段，是一个个人爱好项目。这意味着开发进度可能会比较缓慢，API可能会有较大变化。

## 如何贡献

### 报告问题

如果您发现了bug或有新功能的建议，请在GitHub上[创建一个issue](https://github.com/yourusername/gneiss-engine/issues)。请尽可能详细地描述问题或建议，包括：

- 对于bug：详细的复现步骤、预期行为和实际行为
- 对于功能请求：详细的功能描述、使用场景和潜在的实现方法

### 提交代码

目前，由于项目处于早期阶段，我们主要接受bug修复和小型改进的pull request。如果您想贡献代码，请按照以下步骤操作：

1. Fork仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建一个Pull Request

### 代码风格

我们使用以下工具来保持代码质量和一致性：

- [Black](https://github.com/psf/black) 用于代码格式化
- [isort](https://github.com/PyCQA/isort) 用于导入排序
- [flake8](https://github.com/PyCQA/flake8) 用于代码质量检查

请确保您的代码通过这些工具的检查。您可以通过以下命令安装这些工具：

```bash
pip install black isort flake8
```

然后，在提交代码之前运行：

```bash
black .
isort .
flake8
```

### 测试

请为您的代码添加适当的测试。我们使用`unittest`框架进行测试。您可以通过以下命令运行测试：

```bash
python -m unittest discover tests
```

## 开发环境设置

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/gneiss-engine.git
cd gneiss-engine
```

2. 创建并激活虚拟环境（可选但推荐）：

```bash
# 使用venv
python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate

# 或者使用conda
conda create -n gneiss-env python=3.9
conda activate gneiss-env
```

3. 安装开发依赖：

```bash
pip install -e ".[dev]"
```

## 文档

如果您对文档有改进，我们也非常欢迎。文档位于`docs`目录中，使用Markdown格式编写。

## 行为准则

请尊重所有项目参与者。我们希望创建一个友好、包容的环境，让每个人都能舒适地参与。

## 许可证

通过贡献代码，您同意您的贡献将在MIT许可证下发布。