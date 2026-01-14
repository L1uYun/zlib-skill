---
name: zlib
description: 当用户要求 "从 Z-Library 下载书籍"、"搜索 zlib"、"转换电子书为 PDF" 或 "上传到 NotebookLM" 时使用。用于自动化书籍获取和 AI 分析流程。
---

# Z-Library + NotebookLM 技能

通过 Telegram Bot 下载书籍 → 转换为 PDF → 上传到 NotebookLM 进行问答和内容生成。

**重要提示**: 所有命令必须在技能根目录下执行。Agent 应首先找到并 `cd` 进入技能目录 (例如 `~/.claude/skills/zlib` 或用户安装的位置)。

## 快速参考

| 任务 | 命令 (需在技能目录下执行) |
|------|---------------------------|
| **登录 Telegram** | `.venv/Scripts/python scripts/auth_step1_request_code.py` |
| **下载书籍** | `.venv/Scripts/python scripts/zlib_client.py --title "书名"` |
| **转换 PDF** | `.venv/Scripts/python scripts/calibre_convert.py "文件路径"` |
| **上传/使用** | `.venv/Scripts/notebooklm ...` |

> **注意**: Linux/Mac 请使用 `.venv/bin/python`。

## 常见任务

### 1. 自动初始化与认证 (Auto-Setup)

**当执行任务失败 (如报错 "Missing env" 或 "Unauthorized")，或文件 (`.env`, `zlib.session`) 缺失时，必须触发此流程：**

#### 第一步：配置 .env
如果 `.env` 不存在：
1.  使用 `AskUserQuestion` 询问用户的 `TG_API_ID`, `TG_API_HASH`, `TG_PHONE`, `ZLIB_BOT_USER` (例如 @zlibforxxx_bot)。
2.  使用 `Write` 工具将这些内容写入 `.env` 文件。
    ```ini
    TG_API_ID=...
    TG_API_HASH=...
    TG_PHONE=...
    ZLIB_BOT_USER=...
    DOWNLOAD_DIR=downloads
    TG_PROXY=http://127.0.0.1:7890
    ```

#### 第二步：Telegram 认证
如果 `zlib.session` 不存在：
1.  运行发送验证码脚本：
    ```bash
    .venv/Scripts/python scripts/auth_step1_request_code.py
    ```
2.  使用 `AskUserQuestion` 询问用户收到的 5 位验证码。
3.  运行提交脚本：
    ```bash
    .venv/Scripts/python scripts/auth_step2_submit_code.py <用户输入的验证码>
    ```
4.  如果提示 `PASSWORD_NEEDED`，再询问两步验证密码并运行 `scripts/auth_step3_submit_password.py <密码>`。

### 2. 下载书籍 (Download)

直接搜索并下载。**无需**反复确认授权。

```bash
.venv/Scripts/python scripts/zlib_client.py --title "书名"
```

- 如果返回多个结果，列出结果并询问用户选择哪个序号 (使用 `--index N` 重新运行)。
- 如果用户明确指定 (如 "下载第一个结果")，直接加 `--index 1`。

### 3. 完整流程 (All-in-one)

如果用户要求 "下载 X 并上传到 NotebookLM":

1.  **下载**: `python scripts/zlib_client.py --title "X" --index 1`
2.  **转换**: `python scripts/calibre_convert.py <epub文件>`
3.  **创建**: `notebooklm create "X"`
4.  **上传**: `notebooklm source add <pdf文件>`

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `scripts/zlib_client.py` | 下载书籍。支持 `--title` (搜索) 和 `--index` (选择)。无交互模式。 |
| `scripts/auth_step*.py` | 分步登录脚本，适用于非交互环境。 |

## 依赖要求

- `.env` 文件配置正确 (API_ID, HASH, PHONE, BOT_USER)
- Python 3.10+
