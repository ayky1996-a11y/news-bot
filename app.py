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
RSS_SOURCES = [
    "https://nitter.net/spectatorindex/rss",
    "https://nitter.net/FirstSquawk/rss"
]

async def get_smart_prefix(text):
    """Headline ke basis par sahi word aur emoji chunna"""
    t = text.lower()
    
    # 1. Geopolitical / War
    if any(word in t for word in ['war', 'attack', 'strike', 'military', 'iran', 'israel', 'explosion']):
        return "🚨 BREAKING"
    
    # 2. Market / Economy
    if any(word in t for word in ['fed', 'rbi', 'inflation', 'gdp', 'interest rate', 'nifty', 'sensex', 'stock']):
        return "⚡ MARKET ALERT"
    
    # 3. Crypto
    if any(word in t for word in ['bitcoin', 'btc', 'crypto', 'eth', 'binance']):
        return "₿ CRYPTO FLASH"
    
    # 4. Politics
    if any(word in t for word in ['trump', 'election', 'president', 'government', 'white house']):
        return "📰 POLITICAL UPDATE"
    
    # Default
    return "📢 JUST IN"

async def fetch_and_post(bot, url, posted_links, ssl_context):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context) as response:
            content = response.read()
        
        feed = feedparser.parse(content)
        for entry in feed.entries[:5]:
            if entry.link not in posted_links:
                raw_text = entry.title
                clean_text = re.sub(r'Twitter / \w+: ', '', raw_text).strip()
                
                # Smart Prefix chunna
                prefix = await get_smart_prefix(clean_text)
                
                # LMWM Style Formatting
                flash_msg = f"**{prefix}:**\n\n{clean_text}\n\n@trade_with_PEACE1"

                try:
                    # Media check
                    media_url = None
                    if 'media_content' in entry:
                        media_url = entry.media_content[0]['url']
                    
                    if media_url:
                        await bot.send_photo(chat_id=CHANNEL_ID, photo=media_url, caption=flash_msg, parse_mode='Markdown')
                    else:
                        await bot.send_message(chat_id=CHANNEL_ID, text=flash_msg, parse_mode='Markdown', disable_web_page_preview=True)
                    
                    posted_links.add(entry.link)
                    print(f"✅ Posted with prefix '{prefix}': {clean_text[:30]}...")
                except Exception as e:
                    print(f"Send Error: {e}")

    except Exception as e:
        print(f"Fetch Error: {e}")

async def main():
    ssl_context = ssl._create_unverified_context()
    bot = telegram.Bot(token=BOT_TOKEN)
    posted_links = set()
    print("🚀 Smart Prefix Bot Started...")

    while True:
        for source in RSS_SOURCES:
            await fetch_and_post(bot, source, posted_links, ssl_context)
            await asyncio.sleep(5)
        await asyncio.sleep(90) # Check every 1.5 mins

if __name__ == "__main__":
    asyncio.run(main())
