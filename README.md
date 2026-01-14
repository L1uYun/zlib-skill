# zlib-skill

这是一个 Claude Code 技能，集成了 Z-Library 和 NotebookLM，实现从书籍下载到 AI 研读的自动化工作流。

## 功能特性

- **Z-Library 下载**: 通过 Telegram Bot 搜索并下载书籍
- **格式转换**: 自动将 EPUB/MOBI 转换为 PDF (需安装 Calibre)
- **NotebookLM 集成**: 自动上传书籍到 Google NotebookLM
- **AI 研读**: 支持生成播客、摘要、幻灯片，以及通过对话深入研读

## 快速开始

### 1. 安装技能

```bash
# 在 Claude Code 中
/skill-manager install zlib
```

### 2. 初始化配置

详细配置指南请参考 [references/initialization.md](references/initialization.md)。

主要步骤：
1. 配置 Telegram Bot 和 API
2. 填写 `.env`
3. 登录 Telegram 和 NotebookLM

### 3. 使用方法

在 Claude Code 中直接对话：

```
下载《自私的基因》并上传到 NotebookLM
```

或者分步操作：

```
search zlib for "三体"
upload downloads/book.pdf to notebooklm
ask notebooklm "这本书的核心观点是什么？"
```

## 目录结构

```
zlib-skill/
├── SKILL.md                    # 技能入口文件
├── scripts/                    # 核心脚本
│   ├── zlib_client.py         # Telegram 客户端
│   └── calibre_convert.py     # 格式转换工具
├── references/                 # 参考文档
│   ├── initialization.md      # 初始化指南
│   └── notebooklm-cli.md      # CLI 参考
└── requirements.txt            # Python 依赖
```

## 依赖

- Python 3.10+
- Telegram 账号
- Google 账号
- Calibre (可选，用于格式转换)
