---
name: zlib
description: Use this skill when the user wants to search or download books from Z-Library, configure Z-Library credentials, or upload downloaded books to NotebookLM. Handles authentication and interactive book selection.
---

# Z-Library + NotebookLM Interactive Skill

这是一个交互式技能，用于从 Z-Library 获取书籍并利用 AI 进行分析。

## 交互式工作流

Agent 必须遵循以下流程与用户交互，确保顺畅的用户体验。

### 1. 环境检查与初始化 (Setup)

在执行任何任务前，**必须**检查 `.env` 文件和 `zlib.session` 文件是否存在于技能根目录。

**如果缺少 .env 配置**:
1.  **询问配置**: 使用 `AskUserQuestion` 依次或一次性获取用户的 `TG_API_ID`, `TG_API_HASH`, `TG_PHONE` (格式 +86...), `ZLIB_BOT_USER` (例如 @zlib_bot)。
2.  **保存配置**: 使用 `Write` 工具将这些内容写入 `.env` 文件（参考原有格式）。

**如果缺少 zlib.session (未登录)**:
1.  **请求验证码**: 运行 `.venv/Scripts/python scripts/auth.py request` (Linux/Mac 用 `.venv/bin/python`)。
2.  **询问验证码**: **立即**使用 `AskUserQuestion` 询问用户 "请输入您收到的 Telegram 5 位登录验证码"。
3.  **提交验证码**: 运行 `.venv/Scripts/python scripts/auth.py submit <用户输入的验证码>`。
4.  **二步验证 (如果需要)**: 如果脚本输出提示需要密码，使用 `AskUserQuestion` 询问密码，然后运行 `.venv/Scripts/python scripts/auth.py 2fa <密码>`。

### 2. 下载书籍 (Download)

当用户请求搜索或下载书籍时：

1.  **执行搜索**:
    运行命令: `.venv/Scripts/python scripts/zlib_client.py --title "用户提供的书名"`

2.  **解析输出并交互**:
    *   **直接下载成功**: 如果输出最后一行是文件路径，则跳过此步。
    *   **未找到结果**: 如果输出提示 "No results" 或类似信息，告知用户未找到该书，并询问是否要搜索其他关键词。
    *   **需要用户选择**: 如果输出包含编号列表 (如 `[1] 书名...`) 和提示信息：
        1.  **提取选项**: 从输出中解析出书籍列表。
        2.  **询问用户**: 使用 `AskUserQuestion` (建议使用 `multiSelect: false` 的选择题形式，或者简单的文本回答) 让用户选择一本。
            *   *示例提问*: "找到了以下书籍，请选择您想下载的序号："
        3.  **再次执行**: 根据用户选择的序号 (例如 `N`)，重新运行命令：
            `.venv/Scripts/python scripts/zlib_client.py --title "用户提供的书名" --index N`

### 3. 转换与上传 (Convert & Upload)

下载成功获得文件路径后，根据用户意图执行：

*   **转换为 PDF**:
    运行 `.venv/Scripts/python scripts/calibre_convert.py "文件路径"`
    *注意*: 只有当用户需要 PDF 或后续要上传到 NotebookLM 时才执行此步。

*   **上传到 NotebookLM**:
    1.  如果需要创建新笔记本: `notebooklm create "笔记本名称"`
    2.  上传文件: `notebooklm source add "PDF文件路径"`

## 常用命令参考

所有命令均需在技能根目录下执行。Windows 使用 `.venv/Scripts/python`，Linux/Mac 使用 `.venv/bin/python`。

| 任务 | 命令 |
|------|------|
| **搜索/下载** | `python scripts/zlib_client.py --title "书名" [--index N]` |
| **转换 PDF** | `python scripts/calibre_convert.py "source_file"` |
| **登录 Step 1** | `python scripts/auth.py request` |
| **登录 Step 2** | `python scripts/auth.py submit <code>` |
| **登录 Step 3** | `python scripts/auth.py 2fa <password>` |

## 故障排除

*   **ModuleNotFoundError**: 确保使用了虚拟环境中的 Python (`.venv/...`).
*   **AuthKeyUnregistered / SessionRevoked**: 删除 `zlib.session` 文件，并重新执行“环境检查与初始化”中的登录流程。
*   **Timeout**: Telegram 连接可能不稳定，请检查 `TG_PROXY` 设置是否正确 (在 `.env` 中)。
