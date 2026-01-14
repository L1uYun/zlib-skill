import argparse
import asyncio
import os
import pickle
import sys
from pathlib import Path
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv

# Add scripts dir to path to import utils
sys.path.append(str(Path(__file__).parent))
from utils import get_proxy

base_dir = Path(__file__).resolve().parent.parent
load_env_path = base_dir / ".env"
load_dotenv(load_env_path)

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")
phone = os.getenv("TG_PHONE")
session_path = base_dir / "zlib.session"
phone_hash_path = Path("phone_hash.pkl")

async def request_code(client: TelegramClient):
    print(f"Sending code to {phone}...")
    sent = await client.send_code_request(phone)
    # Save phone_code_hash to temp file
    with open(phone_hash_path, "wb") as f:
        pickle.dump(sent.phone_code_hash, f)
    print("Code sent! Please check your Telegram app.")

async def submit_code(client: TelegramClient, code: str):
    if not phone_hash_path.exists():
        print("Error: Please run 'request' step first")
        sys.exit(1)

    with open(phone_hash_path, "rb") as f:
        phone_code_hash = pickle.load(f)

    try:
        await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
        print("Login successful!")
        # Clean up
        if phone_hash_path.exists():
            os.remove(phone_hash_path)
    except SessionPasswordNeededError:
        print("PASSWORD_NEEDED")
        # Don't clean up hash yet, might need it? actually sign_in usually consumes it or session state handles it.
        # But for SessionPasswordNeededError, we just need to provide password next.

async def submit_password(client: TelegramClient, password: str):
    try:
        await client.sign_in(password=password)
        print("Login successful!")
        if phone_hash_path.exists():
            os.remove(phone_hash_path)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Telegram Authentication Helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Step 1: Request code
    subparsers.add_parser("request", help="Request authentication code")

    # Step 2: Submit code
    submit_parser = subparsers.add_parser("submit", help="Submit authentication code")
    submit_parser.add_argument("code", help="The 5-digit code received")

    # Step 3: Submit 2FA password (if needed)
    password_parser = subparsers.add_parser("2fa", help="Submit 2FA password")
    password_parser.add_argument("password", help="Your 2FA password")

    args = parser.parse_args()

    if not api_id or not api_hash or not phone:
        print("Error: TG_API_ID, TG_API_HASH, or TG_PHONE not found in .env")
        sys.exit(1)

    proxy = get_proxy()
    # Convert api_id to int
    try:
        api_id_int = int(api_id)
    except ValueError:
        print("Error: TG_API_ID must be an integer")
        sys.exit(1)

    client = TelegramClient(str(session_path), api_id_int, api_hash, proxy=proxy)

    await client.connect()

    if args.command == "request":
        if not await client.is_user_authorized():
            await request_code(client)
        else:
            print("Already authorized")
    elif args.command == "submit":
        await submit_code(client, args.code)
    elif args.command == "2fa":
        await submit_password(client, args.password)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
