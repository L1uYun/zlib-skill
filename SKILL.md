---
name: zlib
description: 当用户要求 "从 Z-Library 下载书籍"、"搜索 zlib"、"转换电子书为 PDF" 或 "上传到 NotebookLM" 时使用。用于自动化书籍获取和 AI 分析流程。
---

# Z-Library + NotebookLM 技能

通过 Telegram Bot 下载书籍 → 转换为 PDF → 上传到 NotebookLM 进行问答和内容生成。

## 安全提示

仅限授权的个人使用，必须经用户确认。拒绝批量下载或滥用凭据。

## 快速参考

| 步骤 | Windows 命令 (示例) | 说明 |
|------|---------------------|------|
| 下载 | `.venv/Scripts/python scripts/zlib_client.py --title "书名"` | 搜索并下载 |
| 转换 | `.venv/Scripts/python scripts/calibre_convert.py downloads/book.epub` | 需安装 Calibre |
| 创建笔记本 | `.venv/Scripts/notebooklm create "标题"` | 新建笔记本 |
| 上传 PDF | `.venv/Scripts/notebooklm source add "file.pdf"` | 添加来源 |
| 提问 | `.venv/Scripts/notebooklm ask "问题"` | AI 对话 |
| 生成音频 | `.venv/Scripts/notebooklm generate audio` | 生成播客 |

> **注意**: Linux/Mac 用户请使用 `.venv/bin/python` 替代 `.venv/Scripts/python`。

## 工作流

### 1. 下载书籍

```bash
.venv/Scripts/python scripts/zlib_client.py --title "三体"
# 指定序号下载: --index 1
```

下载到 `downloads/` 目录。如果不指定 `--index`，将列出搜索结果并退出。

### 2. 转换为 PDF (如有需要)

```bash
.venv/Scripts/python scripts/calibre_convert.py downloads/book.epub
```

需要系统已安装 Calibre 并配置路径。

### 3. 上传到 NotebookLM

```bash
.venv/Scripts/notebooklm create "三体研读"
# 记录返回的 notebook-id
.venv/Scripts/notebooklm use <notebook-id>
.venv/Scripts/notebooklm source add "downloads/book.pdf"
```

### 4. 使用 NotebookLM

```bash
.venv/Scripts/notebooklm ask "这本书的主要观点是什么？"
.venv/Scripts/notebooklm generate audio  # 生成播客
.venv/Scripts/notebooklm generate slide-deck
```

## 首次设置

请参阅 [references/initialization.md](references/initialization.md) 获取完整指南。

**快速检查:**
- `.env` 文件包含 Telegram 凭据
- `zlib.session` 文件 (Telegram 登录状态)
- `~/.notebooklm/storage_state.json` (NotebookLM 登录状态)

## 参考文档

- **[initialization.md](references/initialization.md)** - 初始化配置指南 (中文)
- **[notebooklm-cli.md](references/notebooklm-cli.md)** - CLI 命令参考

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `scripts/zlib_client.py` | Telegram bot 交互客户端 |
| `scripts/calibre_convert.py` | Calibre 格式转换工具 |
| `scripts/auth_step*.py` | Telegram 分步认证脚本 |

## 依赖要求

- Python 3.10+
- Telegram 账号 (已绑定 Z-Library Bot)
- Calibre (用于电子书转换)
- Google 账号 (用于 NotebookLM)
