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

### 1. 登录 (Login)

如果用户要求 "登录" 或 "初始化":
1.  检查 `.env` 是否存在。若不存在，引导用户创建。
2.  **不要**去读 `initialization.md`，直接运行:
    ```bash
    .venv/Scripts/python scripts/auth_step1_request_code.py
    ```
3.  询问用户收到的验证码，然后运行:
    ```bash
    .venv/Scripts/python scripts/auth_step2_submit_code.py <验证码>
    ```
4.  (如果需要密码) 运行 `scripts/auth_step3_submit_password.py <密码>`。

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
