import os
import time
import feedparser
import telegram
import asyncio
import urllib.request

# Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trade_with_PEACE1"
# Best for Indian Stock Market & Finance
RSS_URL = "https://www.moneycontrol.com/rss/business.xml"

async def main():
    bot = telegram.Bot(token=BOT_TOKEN)
    posted_links = set()
    print("Bot started fetching news from Moneycontrol...")

    while True:
        try:
            # Adding Headers to avoid 404/403 errors
            req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read()
            
            feed = feedparser.parse(content)
            
            for entry in feed.entries[:5]:
                if entry.link not in posted_links:
                    message = f"🚨 **MARKET UPDATE**\n\n{entry.title}\n\n{entry.link}"
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
                    posted_links.add(entry.link)
                    print(f"Sent: {entry.title}")
            
            await asyncio.sleep(300) # 5 minute check interval
        except Exception as e:
            print(f"Error occurred: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
