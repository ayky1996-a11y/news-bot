import os
import time
import feedparser
from telegram import Bot
import asyncio
import urllib.request

# Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trade_with_PEACE1"
# Reuters Business working link
RSS_URL = "https://www.reutersagency.com/feed/?best-topics=business&post_type=best-topic"

async def main():
    bot = Bot(token=BOT_TOKEN)
    posted_links = set()
    print("Bot started fetching news...")

    while True:
        try:
            # Adding User-Agent to avoid being blocked
            req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read()
            
            feed = feedparser.parse(content)
            print(f"Found {len(feed.entries)} entries in feed.") # Ise logs mein check karein

            for entry in feed.entries[:5]: # Top 5 news
                if entry.link not in posted_links:
                    message = f"🚨 **MARKET UPDATE**\n\n{entry.title}\n\n{entry.link}"
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
                    posted_links.add(entry.link)
                    print(f"Sent: {entry.title}")
            
            await asyncio.sleep(600) # 10 minute wait
        except Exception as e:
            print(f"Error occurred: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
