import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

if sys.platform.startswith("win"):
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import KeyboardButtonCallback
from telethon.tl.types import Message
from telethon.tl.types import User


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key and value:
            os.environ.setdefault(key, value)


def require_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing env: {key}")
    return value


def get_proxy():
    proxy_str = os.getenv("TG_PROXY")
    if not proxy_str:
        return None
    parsed = urlparse(proxy_str)
    if not parsed.scheme or not parsed.hostname or not parsed.port:
        return None
    proxy_type = parsed.scheme.lower()
    if proxy_type not in {"socks5", "http"}:
        return None
    proxy = {
        "proxy_type": proxy_type,
        "addr": parsed.hostname,
        "port": parsed.port,
        "rdns": True,
    }
    if parsed.username and parsed.password:
        proxy["username"] = parsed.username
        proxy["password"] = parsed.password
    return proxy


def parse_results(text: str) -> list[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    results = []
    for ln in lines:
        if re.match(r"^\d+\.", ln):
            results.append(ln)
            continue
        if ln.startswith("📚"):
            results.append(ln.replace("📚", "", 1).strip())
    return results


def parse_book_ids(text: str) -> list[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    book_ids = []
    for ln in lines:
        match = re.match(r"^/book\S+", ln)
        if match:
            book_ids.append(match.group(0))
    return book_ids


def choose_index(results: list[str], provided: int | None) -> int:
    for i, item in enumerate(results, start=1):
        safe_item = item.encode("utf-8", errors="ignore").decode("utf-8")
        print(f"[{i}] {safe_item}")
    if provided is None:
        print("请重新运行命令并添加 --index <序号> 参数来下载。")
        sys.exit(0)
    else:
        idx = provided
    if idx < 1 or idx > len(results):
        raise RuntimeError("Invalid choice")
    return idx - 1


def find_buttons(msg: Message) -> list[KeyboardButtonCallback]:
    buttons = []
    if not msg.buttons:
        return buttons
    for row in msg.buttons:
        for btn in row:
            if isinstance(btn, KeyboardButtonCallback):
                buttons.append(btn)
    return buttons


async def login_only(client: TelegramClient, phone: str) -> None:
    try:
        await client.start(phone=phone)
    except SessionPasswordNeededError:
        print("需要二步验证密码，请重新运行并输入密码")
        raise


def resolve_user_id(entity) -> int:
    if isinstance(entity, User):
        return entity.id
    return int(getattr(entity, "user_id", 0) or 0)


import asyncio

async def wait_new_message(client: TelegramClient, peer, min_id: int, timeout: int = 60) -> Message:
    """Wait for a new message from peer with id > min_id."""
    for _ in range(timeout):
        messages = await client.get_messages(peer, limit=1)
        if messages:
            msg = messages[0]
            if msg.id > min_id and resolve_user_id(msg.sender) == resolve_user_id(peer):
                return msg
        await asyncio.sleep(1)
    raise TimeoutError("Timeout waiting for bot response")


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", help="book title")
    parser.add_argument("--index", type=int, help="result index (1-based)")
    parser.add_argument("--login", action="store_true")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    load_env(base_dir / ".env")

    api_id = int(require_env("TG_API_ID"))
    api_hash = require_env("TG_API_HASH")
    phone = require_env("TG_PHONE")
    bot_user = require_env("ZLIB_BOT_USER")
    download_dir = Path(os.getenv("DOWNLOAD_DIR", "downloads"))
    if not download_dir.is_absolute():
        download_dir = base_dir / download_dir

    # Ensure download directory exists
    download_dir.mkdir(exist_ok=True)

    session_path = base_dir / "zlib.session"
    proxy = get_proxy()
    client = TelegramClient(str(session_path), api_id, api_hash, proxy=proxy, connection_retries=10, retry_delay=1)

    async with client:
        if args.login:
            await login_only(client, phone)
            print("Telethon 登录完成")
            return
        if not args.title:
            raise RuntimeError("Missing --title")

        entity = await client.get_entity(bot_user)
        bot_id = resolve_user_id(entity)

        # Get last message id to filter new messages
        last_msgs = await client.get_messages(entity, limit=1)
        last_id = last_msgs[0].id if last_msgs else 0

        await client.send_message(entity, args.title)

        # Wait for search results
        msg = await wait_new_message(client, entity, last_id)
        last_id = msg.id  # Update last_id

        text = msg.raw_text or ""

        results = parse_results(text)
        if not results:
            print(text)
            raise RuntimeError("No results")

        idx = choose_index(results, args.index)
        book_ids = parse_book_ids(text)
        if idx >= len(book_ids):
            raise RuntimeError("Selected index out of range")

        await client.send_message(entity, book_ids[idx])

        # Wait for file
        # Note: Bot might send "uploading..." text before file, so we need to loop
        while True:
            file_msg = await wait_new_message(client, entity, last_id)
            last_id = file_msg.id
            if getattr(file_msg, "file", None):
                break

        file_path = await client.download_media(file_msg, file=download_dir)
        print(file_path)


if __name__ == "__main__":
    try:
        import asyncio

        asyncio.run(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
