<h1 align="center">CodeCapsule</h1>
<h1 align="center">代码胶囊</h1>
<p align="center">
<a href="https://space.bilibili.com/1909782963">
<img src="./docs/imgs/logo.svg" alt="代码胶囊" width="300" />
</a>
</p>
<p align="center"><b>尝试将代码片段整理好</b></p>
## 项目介绍

**CodeCapsule** 是一个基于 PySide6 的桌面代码片段管理工具，旨在帮助开发者高效地组织、存储和检索代码片段。它通过直观的图形界面，将代码片段按项目分组存储，支持多种编程语言和自定义标签，满足从个人学习到团队协作的多种需求。无论是快速记录灵感片段，还是管理复杂的代码库，SnippetVault 都能提供灵活而强大的支持。

**CodeCapsule** 是一个轻量级、跨平台的代码片段管理工具，使用 PySide6 构建。它允许用户以文件夹和项目的形式组织代码片段，支持多种文件类型（txt、Python、Java、Bash 等）和自定义标签，方便快速检索和管理。


## 功能特性

- **层次化管理**：支持主文件夹 > 项目 > 代码片段的结构，与文件系统直接对应。
- **代码片段属性**：
  - 文件名：自定义命名。
  - 标签：如 "python"、"django"、"fastapi"，支持多标签。
  - 代码类型：识别 "txt"、"python"、"java"、"bash" 等格式。
- **增删改查**：
  - 创建新项目和代码片段。
  - 编辑代码内容及元数据。
  - 删除项目或代码片段。
  - 查看代码片段列表及其详细信息。
- **直观界面**：基于 PySide6 的现代 GUI，包含树状视图、表格视图和编辑窗口。
- **元数据管理**：每个项目的代码片段属性存储在 `metadata.json` 中。
- **附加功能**（计划中）：
  - 按标签或文件名过滤代码片段。
  - 全局搜索功能。
  - 代码高亮显示。

## 安装

### 前置条件
- Python 3.8 或更高版本
- PySide6（Qt for Python）

### 安装步骤
1. 克隆仓库：
   ```bash
   git clone https://github.com/cpython666/CodeCapsule.git
   cd CodeCapsule
```
2. 创建虚拟环境（可选但推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. 安装依赖：
   ```bash
   pip install PySide6
   ```
4. 运行程序：
   ```bash
   python main.py
   ```

## 使用说明

1. **启动程序**：运行 `main.py`，主窗口将显示。
2. **选择主文件夹**：通过“文件”菜单选择一个根目录，用于存储所有项目。
3. **管理项目**：
   - 在左侧树视图中浏览项目和代码片段。
   - 右键或通过按钮创建新项目。
4. **管理代码片段**：
   - 选中项目后，右侧表格显示该项目的代码片段列表。
   - 点击代码片段查看和编辑内容、标签及代码类型。
   - 点击“保存”更新更改。
5. **自定义**：根据需要调整标签或代码类型。

## 项目结构

```
CodeCapsule/
├── main.py           # 主程序入口
├── snippet_manager.py # 核心逻辑类
├── README.md         # 项目说明
└── screenshot.png    # 示例截图（可选）
```

每个项目文件夹内：
```
project_folder/
├── snippet1.py       # 代码片段文件
├── snippet2.sh       # 代码片段文件
└── metadata.json     # 元数据文件
```

## 贡献指南

欢迎为 SnippetVault 贡献代码或提出建议！请按照以下步骤参与：

1. Fork 本仓库。
2. 创建你的功能分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. 提交更改：
   ```bash
   git commit -m "Add your feature"
   ```
4. Push 到你的分支：
   ```bash
   git push origin feature/your-feature-name
   ```
5. 提交 Pull Request。

### 待办事项
- 添加代码高亮支持。
- 实现全局搜索功能。
- 支持多语言界面。
- 集成代码片段截图
- 文件夹拖拽导入
- github备份文件夹
- 公开代码片段到CodeHub

## 许可证

本项目采用 [MIT 许可证](LICENSE) 开源。

## 联系方式

有问题或建议？请通过 [GitHub Issues](https://github.com/cpython666/CodeCapsule/issues) 联系我们，或发送邮件至 your.email@example.com。

