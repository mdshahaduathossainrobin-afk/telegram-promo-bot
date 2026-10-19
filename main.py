import logging
import asyncio
import random
import os
import threading
from flask import Flask
from telethon import TelegramClient, events

# Configure Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

API_ID = 39097979
API_HASH = 'f23c7abd6d08744a52da529dd566f1f9'

client = TelegramClient('user_session', API_ID, API_HASH)
TARGET_CHANNEL = 'klyx_news'

# Dummy Web Server to satisfy Render Web Service Port Requirement
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Promo Auto-Claimer is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

@client.on(events.NewMessage(chats=TARGET_CHANNEL))
async def promo_handler(event):
    if not event.message.buttons:
        return

    for row in event.message.buttons:
        for button in row:
            if button.text and "Activate in bot" in button.text:
                random_delay = round(random.uniform(0.35, 0.65), 3)
                logging.info(f"🎯 Target Promo Found! Waiting {random_delay}s...")
                
                await asyncio.sleep(random_delay)

                try:
                    await button.click()
                    logging.info("⚡ Successfully activated via bot!")
                except Exception as e:
                    logging.error(f"⚠️ Activation failed / Slot full: {e}")
                
                logging.info("👀 Returned to listening mode in @klyx_news...")
                return

async def main():
    # Start Dummy Web Server in Background Thread
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("🚀 Safe Auto-Claimer Running...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
    
