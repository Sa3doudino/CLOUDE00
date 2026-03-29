import asyncio
import os
import math
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID   = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]
SESSION  = os.environ["TG_SESSION"]

CHUNK    = int(1.9 * 1024**3)

async def main():
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()

    filepath = os.environ.get("FILE_PATH", "target_file")
    chat     = os.environ.get("TG_CHAT", "me")
    filename = os.path.basename(filepath)
    size     = os.path.getsize(filepath)
    total    = math.ceil(size / CHUNK)

    print(f"الملف: {filename}")
    print(f"الحجم: {size / 1024**3:.2f} GB")
    print(f"الاجزاء: {total}")

    with open(filepath, "rb") as f:
        for i in range(total):
            chunk = f.read(CHUNK)
            part  = f"part_{i+1:03d}_{filename}"

            with open(part, "wb") as p:
                p.write(chunk)

            print(f"رفع {i+1}/{total}...")

            await client.send_file(
                chat,
                part,
                caption=f"{filename} | Part {i+1}/{total}"
            )

            os.remove(part)
            print(f"{i+1}/{total} تم!")

    print("كلشي تم بنجاح!")
    await client.disconnect()

asyncio.run(main())
