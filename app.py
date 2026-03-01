import os
import feedparser
import telegram
import asyncio
import urllib.request
import ssl
import re

# --- Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trade_with_PEACE1"

# Different instances use kar rahe hain taaki agar ek block ho toh doosra chale
RSS_SOURCES = [
    "https://nitter.cz/spectatorindex/rss",
    "https://nitter.it/FirstSquawk/rss",
    "https://nitter.privacydev.net/disclosetv/rss"
]

async def get_smart_prefix(text):
    t = text.lower()
    if any(word in t for word in ['war', 'attack', 'strike', 'military', 'iran', 'israel', 'explosion']):
        return "🚨 BREAKING"
    if any(word in t for word in ['fed', 'rbi', 'inflation', 'gdp', 'interest rate', 'nifty', 'sensex', 'stock']):
        return "⚡ MARKET ALERT"
    if any(word in t for word in ['bitcoin', 'btc', 'crypto', 'eth', 'binance']):
        return "₿ CRYPTO FLASH"
    if any(word in t for word in ['trump', 'election', 'president', 'government', 'white house']):
        return "📰 POLITICAL UPDATE"
    return "📢 JUST IN"

async def fetch_and_post(bot, url, posted_links, ssl_context):
    try:
        # Timeout add kiya hai taaki bot hang na ho
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36'})
        with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
            content = response.read()
        
        feed = feedparser.parse(content)
        if not feed.entries:
            print(f"⚠️ No entries found for {url}")
            return

        for entry in feed.entries[:5]:
            if entry.link not in posted_links:
                raw_text = entry.title
                # Twitter formatting saaf karna
                clean_text = re.sub(r'Twitter / \w+: ', '', raw_text).strip()
                
                if clean_text:
                    prefix = await get_smart_prefix(clean_text)
                    flash_msg = f"**{prefix}:**\n\n{clean_text}\n\n@trade_with_PEACE1"

                    try:
                        # Media detection
                        media_url = None
                        if 'media_content' in entry:
                            media_url = entry.media_content[0]['url']
                        
                        if media_url:
                            await bot.send_photo(chat_id=CHANNEL_ID, photo=media_url, caption=flash_msg, parse_mode='Markdown')
                        else:
                            await bot.send_message(chat_id=CHANNEL_ID, text=flash_msg, parse_mode='Markdown', disable_web_page_preview=True)
                        
                        posted_links.add(entry.link)
                    except Exception as e:
                        print(f"Post Error: {e}")

    except Exception as e:
        print(f"Fetch Error from {url}: {e}")

async def main():
    ssl_context = ssl._create_unverified_context()
    bot = telegram.Bot(token=BOT_TOKEN)
    posted_links = set()
    print("🚀 Smart Prefix Bot Started with Multi-Source Support...")

    while True:
        for source in RSS_SOURCES:
            await fetch_and_post(bot, source, posted_links, ssl_context)
            await asyncio.sleep(10) # Sources ke beech thoda gap
        
        print("⏳ Cycle complete. Waiting 2 minutes...")
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())
