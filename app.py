import os
import feedparser
import telegram
import asyncio
import urllib.request
import ssl
import re
from datetime import datetime, timedelta
import time

# --- Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trade_with_PEACE1"

# Fresh and Stable Sources
RSS_SOURCES = [
    "https://www.investing.com/rss/news_285.rss", 
    "https://www.investing.com/rss/market_overview_investing_ideas.rss",
    "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best-topic"
]

async def get_smart_prefix(text):
    t = text.lower()
    if any(word in t for word in ['war', 'attack', 'strike', 'military', 'iran', 'israel', 'explosion']):
        return "🚨 BREAKING"
    if any(word in t for word in ['fed', 'rbi', 'inflation', 'interest rate', 'nifty', 'stock', 'market']):
        return "⚡ MARKET ALERT"
    if any(word in t for word in ['bitcoin', 'btc', 'crypto', 'eth']):
        return "₿ CRYPTO FLASH"
    return "📢 JUST IN"

async def fetch_and_post(bot, url, posted_links, ssl_context):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context, timeout=20) as response:
            content = response.read()
        
        feed = feedparser.parse(content)
        current_time = datetime.now()

        for entry in feed.entries:
            if entry.link not in posted_links:
                # --- TIME FILTER LOGIC ---
                # News kab publish hui thi, usse check karna
                published_time = None
                if 'published_parsed' in entry:
                    published_time = datetime(*entry.published_parsed[:6])
                
                # Sirf wahi news bhejni hai jo pichle 24 ghanton mein aayi ho
                if published_time and (current_time - published_time) > timedelta(hours=24):
                    continue 

                title = entry.title
                prefix = await get_smart_prefix(title)
                flash_msg = f"**{prefix}:**\n\n{title}\n\n@trade_with_PEACE1"

                try:
                    media_url = entry.media_content[0]['url'] if 'media_content' in entry else None
                    
                    if media_url:
                        await bot.send_photo(chat_id=CHANNEL_ID, photo=media_url, caption=flash_msg, parse_mode='Markdown')
                    else:
                        await bot.send_message(chat_id=CHANNEL_ID, text=flash_msg, parse_mode='Markdown', disable_web_page_preview=True)
                    
                    posted_links.add(entry.link)
                    print(f"✅ Success: {title[:40]}...")
                except Exception as e:
                    print(f"Post Error: {e}")

    except Exception as e:
        print(f"Fetch Error: {e}")

async def main():
    ssl_context = ssl._create_unverified_context()
    bot = telegram.Bot(token=BOT_TOKEN)
    posted_links = set()
    print("🚀 Fresh News Bot Started (24h Filter Active)...")

    while True:
        for source in RSS_SOURCES:
            await fetch_and_post(bot, source, posted_links, ssl_context)
            await asyncio.sleep(10)
        await asyncio.sleep(300) 

if __name__ == "__main__":
    asyncio.run(main())
