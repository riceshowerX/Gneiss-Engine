# 贡献指南

感谢您考虑为 Gneiss-Engine 做出贡献！本指南将帮助您了解如何为项目做出贡献。

## 行为准则

我们致力于为所有贡献者提供友好、尊重和包容的环境。请阅读并遵守我们的行为准则。

## 如何贡献

### 报告 Bug

如果您发现了一个 bug，请先检查是否已经有相关的 issue。如果没有，请创建一个新的 issue，包含以下信息：

- 清晰的标题和描述
- 重现步骤
- 期望的行为
- 实际的行为
- 相关的日志或截图
- 您的环境信息（Python 版本、操作系统等）

### 建议新功能

我们欢迎新功能的建议！请创建一个 issue 来描述：

- 您想要的功能
- 为什么需要这个功能
- 您建议的实现方式（如果有的话）

### 提交 Pull Request

1. Fork 这个仓库
2. 创建一个新的分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/gneiss-engine.git
cd gneiss-engine
```

### 2. 安装依赖

```bash
pip install -e .[dev]
```

### 3. 设置预提交钩子

```bash
pre-commit install
```

## 代码风格

我们使用以下工具来保持代码风格的一致性：

- **Black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码风格检查
- **mypy**: 类型检查

在提交代码之前，请确保运行：

```bash
black gneiss/ tests/ examples/
isort gneiss/ tests/ examples/
flake8 gneiss/ tests/ examples/
mypy gneiss/
```

或者使用预提交钩子自动处理。

## 测试

### 运行测试

```bash
pytest tests/ -v
```

### 测试覆盖率

```bash
pytest tests/ --cov=gneiss --cov-report=html
```

### 编写测试

- 为所有新功能编写测试
- 测试应该覆盖正常情况和边界情况
- 使用描述性的测试名称
- 遵循 AAA 模式 (Arrange-Act-Assert)

## 文档

### 代码文档

- 为所有公共函数和类编写 docstring
- 使用 Google 风格的 docstring 格式
- 包含参数、返回值和异常的描述

### 用户文档

- 更新 README.md 和中文文档
- 添加使用示例
- 保持文档与代码同步

## 提交信息规范

我们使用约定式提交 (Conventional Commits)：

- `feat`: 新功能
- `fix`: bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat: 添加图像旋转功能
fix: 修复水印位置计算错误
docs: 更新安装指南
```

## 代码审查流程

1. 所有 Pull Request 都需要通过代码审查
2. 至少需要一个维护者的批准才能合并
3. 确保所有测试通过
4. 确保代码风格符合规范
5. 确保文档已更新

## 发布流程

1. 更新版本号 (`pyproject.toml`)
2. 更新 CHANGELOG.md
3. 创建发布标签
4. 构建和发布包

## 问题与支持

如果您在贡献过程中遇到任何问题，请：

1. 查看现有的 issue
2. 在 Discord 或 Slack 频道中提问
3. 发送邮件到维护团队

## 许可证

通过向本项目贡献代码，您同意您的贡献将根据项目的 MIT 许可证进行授权。

感谢您的贡献！🎉