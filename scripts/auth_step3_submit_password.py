import asyncio
import argparse
import os
import sys
from pathlib import Path
from telethon import TelegramClient
from dotenv import load_dotenv

# Add scripts dir to path to import utils
sys.path.append(str(Path(__file__).parent))
from utils import get_proxy

base_dir = Path(__file__).resolve().parent.parent
load_env_path = base_dir / ".env"
load_dotenv(load_env_path)

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
session_path = base_dir / "zlib.session"

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("password", help="2FA Password")
    args = parser.parse_args()

    proxy = get_proxy()
    client = TelegramClient(str(session_path), api_id, api_hash, proxy=proxy)
    await client.connect()

    try:
        await client.sign_in(password=args.password)
        print("Login successful!")
        if Path("phone_hash.pkl").exists():
            os.remove("phone_hash.pkl")
    except Exception as e:
        print(f"Error: {e}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
