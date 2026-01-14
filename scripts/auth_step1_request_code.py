import asyncio
import os
import pickle
from pathlib import Path
from telethon import TelegramClient
from dotenv import load_dotenv
import sys

# Add scripts dir to path to import utils
sys.path.append(str(Path(__file__).parent))
from utils import get_proxy

base_dir = Path(__file__).resolve().parent.parent
load_env_path = base_dir / ".env"
load_dotenv(load_env_path)

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
phone = os.getenv("TG_PHONE")
session_path = base_dir / "zlib.session"

async def main():
    proxy = get_proxy()
    client = TelegramClient(str(session_path), api_id, api_hash, proxy=proxy)
    await client.connect()

    if not await client.is_user_authorized():
        print(f"Sending code to {phone}...")
        sent = await client.send_code_request(phone)
        # Save phone_code_hash to temp file
        with open("phone_hash.pkl", "wb") as f:
            pickle.dump(sent.phone_code_hash, f)
        print("Code sent!")
    else:
        print("Already authorized")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
