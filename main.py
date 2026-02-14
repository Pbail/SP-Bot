import asyncio
import sys
import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
## ------------------- Your Telegram API details -------------------
API_ID = 30244162    
API_HASH = "e1472f0be4635de52c95a2e49a3bc5d6"
SESSION_STRING = "1BJWap1wBu50yNJ8LD1Kj4ETVErVSkrjSW9B54R1OUrGDpDMBvUlEkVqOs2J2FXQaWKOEwUxVJS0lBwj61SQNYsEQNtgyswbaCYkaWOTuggjND39s3S-4Mygr63hijpEbmWqJu3i8tY6ve7sH-GgTMHsF2iwp7GouhbNyMhHenJ61lvDXTxnzN4WfAnTTD-72gL_EcH757xxCT3OwhMoNraK1Ex9I4djpxjDJABkhl9VCQjK5JTRDjo_QccVsrS4dm4MIo4sI5OlrV5aFna8SPTdAhwIZxrTIQBxhY_LwTuW0uS4tD0TXePLzZRdEWnnmGbEw5_HZXAJp8s08rFndr4jAuok1Nds="
# ----------------------------------------------------------------------------------------------------------------

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# To track which users got a reply today
last_replied = {}

async def get_saved_messages(limit=6):
    """Fetch the latest saved messages from 'Saved Messages'."""
    messages = []
    async for msg in client.iter_messages('me', limit=limit):
        if msg:
            messages.append(msg)
    return list(reversed(messages))  # oldest first

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    user_id = sender.id
    today = datetime.datetime.now().date()

    # Check if already replied today
    if user_id in last_replied and last_replied[user_id] == today:
        print(f"Already replied to {sender.first_name} today — skipping.")
        return

    print(f"Replying to {sender.first_name} ({user_id})")

    # Get current saved messages
    saved_messages = await get_saved_messages(limit=6)

    # Send each message without "forwarded from"
    for msg in saved_messages:
        try:
            if msg.message and not msg.media:
                await client.send_message(event.chat_id, msg.message)
            else:
                await client.send_file(event.chat_id, msg.media, caption=msg.message)
            await asyncio.sleep(1)  # small delay to avoid flood
        except Exception as e:
            print(f"Error sending message {msg.id}: {e}")

    last_replied[user_id] = today

async def main():
    await client.start()

    if not SESSION_STRING:
        print("✅ First run: save this session string for next time:")
        print(client.session.save())

    print("Userbot is running...")
    await client.run_until_disconnected()

# ---------- macOS asyncio fix ----------
if sys.platform == "darwin":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
else:
    asyncio.run(main())
