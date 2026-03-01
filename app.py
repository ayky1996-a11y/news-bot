import os
import feedparser
import telegram
import asyncio
import urllib.request
import ssl
import re

# --- Config ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trade_with_PEACE1"

# Aap jitne chahe Twitter accounts yahan add kar sakte hain (Nitter use karke)
RSS_SOURCES = [
    "https://nitter.net/spectatorindex/rss",
    "https://nitter.net/FirstSquawk/rss",
    "https://nitter.net/disclosetv/rss"
]

# Market-moving Keywords
KEYWORDS = ['war', 'iran', 'israel', 'trump', 'attack', 'breaking', 'just in', 'crude', 'oil', 'bitcoin', 'fed', 'nuclear']

async def fetch_and_post(bot, url, posted_links, ssl_context):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context) as response:
            content = response.read()
        
        feed = feedparser.parse(content)
        for entry in feed.entries[:5]:
            if entry.link not in posted_links:
                clean_text = re.sub(r'\(.*?\)', '', entry.title).strip() # Faltu brackets hatana
                
                if any(word in clean_text.lower() for word in KEYWORDS):
                    flash_msg = f"**🚨 JUST IN:**\n\n{clean_text}\n\n@trade_with_PEACE1"
                    await bot.send_message(chat_id=CHANNEL_ID, text=flash_msg, parse_mode='Markdown', disable_web_page_preview=True)
                    posted_links.add(entry.link)
                    print(f"✅ Posted: {clean_text[:50]}...")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

async def main():
    ssl_context = ssl._create_unverified_context()
    bot = telegram.Bot(token=BOT_TOKEN)
    posted_links = set()
    print("🚀 Permanent Free Bridge Started...")

    while True:
        for source in RSS_SOURCES:
            await fetch_and_post(bot, source, posted_links, ssl_context)
            await asyncio.sleep(5) # Source ke beech chota gap
        
        await asyncio.sleep(60) # Har 1 minute mein check

if __name__ == "__main__":
    asyncio.run(main())
