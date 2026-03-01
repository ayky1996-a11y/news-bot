import os
import asyncio
import feedparser
from telegram import Bot

# Railway Variables se data lena
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trade_with_PEACE1"

async def send_market_updates():
    bot = Bot(token=TOKEN)
    print("Bot started fetching news...")
    
    # Isse sirf 1 baar fetch hoga, loop ke liye while use karein
    feed = feedparser.parse("https://feeds.reuters.com/reuters/businessNews")
    
    if feed.entries:
        for entry in feed.entries[:3]: # Top 3 news
            message = f"📢 *Market Update*\n\n{entry.title}\n\n[Read more]({entry.link})"
            try:
                await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
                print(f"Sent: {entry.title}")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(send_market_updates())
