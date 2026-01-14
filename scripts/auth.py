import argparse
import asyncio
import os
import json
import sys
from pathlib import Path
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, ApiIdInvalidError, PhoneCodeInvalidError, PhoneCodeExpiredError
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
auth_state_path = base_dir / "auth_state.json"

def save_auth_state(state):
    with open(auth_state_path, "w") as f:
        json.dump(state, f)

def load_auth_state():
    if auth_state_path.exists():
        with open(auth_state_path, "r") as f:
            return json.load(f)
    return {}

async def request_code(client: TelegramClient):
    print(f"Sending code to {phone}...")
    try:
        sent = await client.send_code_request(phone)
        # Save phone_code_hash to persistent state file
        state = load_auth_state()
        state["phone_code_hash"] = sent.phone_code_hash
        save_auth_state(state)
        print("Code sent! Please check your Telegram app.")
    except ApiIdInvalidError:
        print("Error: The API ID or Hash is invalid. Please check your .env file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error sending code: {e}")
        sys.exit(1)

async def submit_code(client: TelegramClient, code: str):
    state = load_auth_state()
    phone_code_hash = state.get("phone_code_hash")

    if not phone_code_hash:
        print("Warning: phone_code_hash not found in local state.")
        print("Attempting to sign in without hash (this may fail)...")

    try:
        if phone_code_hash:
            await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
        else:
             await client.sign_in(phone, code)

        print("Login successful!")
        # Clean up auth state on success
        if auth_state_path.exists():
            os.remove(auth_state_path)

    except SessionPasswordNeededError:
        print("PASSWORD_NEEDED")
        # Do not clean up state, we need to proceed to 2FA
    except (PhoneCodeInvalidError, PhoneCodeExpiredError) as e:
        print(f"Error: Invalid or expired code ({e}). Please run 'request' again.")
        sys.exit(1)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

async def submit_password(client: TelegramClient, password: str):
    try:
        await client.sign_in(password=password)
        print("Login successful!")
        if auth_state_path.exists():
            os.remove(auth_state_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

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
        print("Error: TG_API_ID must be an integer in .env")
        sys.exit(1)

    client = TelegramClient(str(session_path), api_id_int, api_hash, proxy=proxy)

    try:
        await client.connect()
    except Exception as e:
        print(f"Failed to connect to Telegram: {e}")
        print("Please check your network connection and proxy settings.")
        sys.exit(1)

    if args.command == "request":
        if not await client.is_user_authorized():
            await request_code(client)
        else:
            print("Already authorized")
    elif args.command == "submit":
        # Check if authorized first
        if await client.is_user_authorized():
             print("Already authorized")
        else:
             await submit_code(client, args.code)
    elif args.command == "2fa":
        await submit_password(client, args.password)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
