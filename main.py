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

# Target channel username or keywords
TARGET_CHANNELS = ['klyx_news', 'klyx', 'Klyx']

# Flask Web Server
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Promo Auto-Claimer is Running 24/7!"

@client.on(events.NewMessage())
async def promo_handler(event):
    try:
        chat = await event.get_chat()
        chat_username = getattr(chat, 'username', '') or ''
        chat_title = getattr(chat, 'title', '') or ''

        # Match target channel flexibly
        is_target = any(
            tc.lower() in chat_username.lower() or tc.lower() in chat_title.lower() 
            for tc in TARGET_CHANNELS
        )
        
        if not is_target:
            return

        logging.info(f"📩 New message received from: {chat_title} (@{chat_username})")

        # Search for buttons
        if event.message.buttons:
            for row in event.message.buttons:
                for button in row:
                    btn_text = button.text or ""
                    # Check button text ignoring emojis or case
                    if "activate in bot" in btn_text.lower():
                        random_delay = round(random.uniform(0.35, 0.65), 3)
                        logging.info(f"🎯 Target Promo Button Found: '{btn_text}'! Waiting {random_delay}s...")
                        
                        await asyncio.sleep(random_delay)

                        await button.click()
                        logging.info("⚡ Successfully clicked and activated via bot!")
                        return
    except Exception as e:
        logging.error(f"⚠️ Error handling message: {e}")

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def main_bot():
        print("🚀 Safe Auto-Claimer Running...")
        await client.start()
        await client.run_until_disconnected()
        
    loop.run_until_complete(main_bot())

if __name__ == '__main__':
    threading.Thread(target=run_telegram_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
