# Initialization Guide

首次使用本技能需要完成以下配置。

## 前置条件

在开始之前，请确保你有：

| 条件 | 说明 |
|------|------|
| Z-Library 账号 | 在 [z-lib.gs](https://z-lib.gs) 或镜像站注册 |
| Telegram 账号 | 需要能接收验证码的手机号 |
| Google 账号 | 用于 NotebookLM |
| Python 3.10+ | 运行脚本 |
| Calibre | 电子书格式转换（可选） |

## Step 1: 创建虚拟环境

```bash
cd E:/portable/inbox/zlib-skill  # 替换为你的技能目录
python -m venv .venv
.venv/Scripts/pip.exe install -r requirements.txt
playwright install chromium
```

## Step 2: 配置 Z-Library Telegram Bot

### 2.1 登录 Z-Library 网站

1. 访问 [z-lib.gs](https://z-lib.gs) 或其他可用镜像
2. 登录你的账号
3. 进入个人设置页面

### 2.2 获取专属 Telegram Bot

1. 在 Z-Library 网站找到 "Link to Telegram bot" 或类似选项
2. 点击后会跳转到 Telegram，自动打开你的专属机器人
3. 在 Telegram 中发送 `/start` 启动机器人
4. 按机器人指引完成绑定验证

### 2.3 记录机器人用户名

机器人用户名格式：`@zlibfor<你的ID>_bot`

例如：`@zlibforl1uyun_bot`

**提示**：在 Telegram 中点击机器人头像可查看完整用户名。

## Step 3: 获取 Telegram API 凭据

1. 访问 https://my.telegram.org
2. 输入手机号（格式：`+86 13800138000`）
3. 输入收到的验证码登录
4. 点击 **API development tools**
5. 如果是首次，需要创建应用：
   - **App title**: `zlibrary`（任意）
   - **Short name**: `zlib`（任意）
   - **URL**: 留空
   - **Platform**: `Desktop`
   - **Description**: 留空
6. 点击 Create application
7. 记录生成的 `api_id`（数字）和 `api_hash`（字符串）

**注意**：API 凭据只显示一次，请妥善保存。

## Step 4: 创建 .env 文件

在技能根目录创建 `.env` 文件：

```ini
# Telegram 配置（必填）
TG_API_ID=12345678
TG_API_HASH=abcdef1234567890abcdef1234567890
TG_PHONE=+8613800138000
ZLIB_BOT_USER=@zlibforl1uyun_bot

# 下载目录
DOWNLOAD_DIR=downloads

# Calibre 配置（可选，如果 ebook-convert 不在 PATH 中）
# CALIBRE_PATH="C:\Program Files\Calibre2\ebook-convert.exe"

# 代理配置（可选，如需翻墙）
# TG_PROXY=http://127.0.0.1:7890
```

**字段说明**：

| 字段 | 说明 | 示例 |
|------|------|------|
| TG_API_ID | Step 3 获取的 api_id | `12345678` |
| TG_API_HASH | Step 3 获取的 api_hash | `abcdef...` |
| TG_PHONE | 你的手机号，带国家代码 | `+8613800138000` |
| ZLIB_BOT_USER | Step 2 获取的机器人用户名 | `@zlibforl1uyun_bot` |

## Step 5: 登录 Telegram

由于 Claude 环境限制交互式输入，我们提供分步脚本来完成登录。

### 5.1 发送验证码

```bash
.venv/Scripts/python.exe scripts/auth_step1_request_code.py
```

运行后，Telegram 会收到 5 位数验证码。

### 5.2 提交验证码

```bash
.venv/Scripts/python.exe scripts/auth_step2_submit_code.py <验证码>
```

例如：`.venv/Scripts/python.exe scripts/auth_step2_submit_code.py 12345`

### 5.3 提交两步验证密码（如有）

如果 Step 2 提示 `PASSWORD_NEEDED`，请运行：

```bash
.venv/Scripts/python.exe scripts/auth_step3_submit_password.py <你的密码>
```

成功后生成 `zlib.session` 文件。

## Step 6: 登录 NotebookLM

建议在外部终端运行以下命令进行初始化登录：

```bash
# 在外部 CMD 或 PowerShell 中运行
cd <skill-directory>
.venv/Scripts/notebooklm.exe login
```

1. 浏览器自动打开 NotebookLM 页面
2. 完成 Google 账号登录
3. 看到 NotebookLM 主页后，回到终端按 **Enter** 保存

**注意**：在 Claude 内部直接运行可能因为无法输入回车而导致超时。如果在 Claude 中运行，请确保您已经在浏览器中登录过 Google，然后它可能会自动完成。

认证保存在 `~/.notebooklm/storage_state.json`。

## 验证配置

检查以下文件是否存在：

| 文件 | 说明 |
|------|------|
| `.env` | Telegram 配置 |
| `zlib.session` | Telegram 登录状态 |
| `~/.notebooklm/storage_state.json` | NotebookLM 登录状态 |

全部存在即可开始使用。

## 故障排除

### Telegram 登录失败

| 问题 | 解决方案 |
|------|----------|
| 验证码收不到 | 检查手机号格式，确保带国家代码 |
| FloodWaitError | 请求过于频繁，等待提示的秒数后重试 |
| 连接超时 | 检查网络，或配置 TG_PROXY |

### NotebookLM 登录失败

| 问题 | 解决方案 |
|------|----------|
| 浏览器未打开 | 确保已安装 chromium: `playwright install chromium` |
| 登录后无反应 | 在终端按 Enter 手动保存 |

### Z-Library Bot 无响应

| 问题 | 解决方案 |
|------|----------|
| 发消息无回复 | 确认机器人用户名正确，重新发送 `/start` |
| 搜索无结果 | Z-Library 可能暂时不可用，稍后重试 |
