import os
import time
import feedparser
from telegram import Bot
import asyncio

# Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trade_with_PEACE1"
RSS_URL = "https://feeds.reuters.com/reuters/worldNews"

async def main():
    bot = Bot(token=BOT_TOKEN)
    posted_links = set()
    print("Bot started fetching news...")

    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            for entry in feed.entries[:3]:
                if entry.link not in posted_links:
                    message = f"🚨 **BREAKING NEWS**\n\n{entry.title}\n\n{entry.link}"
                    # Ye line ab sahi se run hogi
                    await bot.send_message(chat_id=CHANNEL_ID, text=message)
                    posted_links.add(entry.link)
                    print(f"Sent: {entry.title}")
            
            await asyncio.sleep(600) # 10 minute ka wait
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
