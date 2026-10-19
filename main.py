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

# Flask Web Server
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Promo Auto-Claimer is Running 24/7!"

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

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def main_bot():
        print("🚀 Safe Auto-Claimer Running...")
        await client.start()
        await client.run_until_disconnected()
        
    loop.run_until_complete(main_bot())

if __name__ == '__main__':
    # Telegram bot কে ব্যাকগ্রাউন্ড থ্রেডে রান করা হলো
    threading.Thread(target=run_telegram_bot, daemon=True).start()
    
    # Flask কে মেইন প্রসেস হিসেবে রান করা হলো যাতে Render সাথে সাথে পোর্ট পেয়ে যায়
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
