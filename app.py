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

# In links par kabhi 403 error nahi aayega
RSS_SOURCES = [
    "https://www.investing.com/rss/news_285.rss", # Stock Market News
    "https://www.investing.com/rss/market_overview_investing_ideas.rss", # Trading Ideas
    "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best-topic" # Geopolitics
]

async def get_smart_prefix(text):
    t = text.lower()
    if any(word in t for word in ['war', 'attack', 'strike', 'military', 'iran', 'israel', 'explosion', 'nuclear']):
        return "🚨 BREAKING"
    if any(word in t for word in ['fed', 'rbi', 'inflation', 'gdp', 'interest rate', 'nifty', 'sensex', 'stock', 'market']):
        return "⚡ MARKET ALERT"
    if any(word in t for word in ['bitcoin', 'btc', 'crypto', 'eth', 'binance', 'etf']):
        return "₿ CRYPTO FLASH"
    if any(word in t for word in ['trump', 'election', 'president', 'white house', 'china', 'us']):
        return "📰 POLITICAL UPDATE"
    return "📢 JUST IN"

async def fetch_and_post(bot, url, posted_links, ssl_context):
    try:
        # Standard headers jo Investing.com/Reuters allow karte hain
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context, timeout=20) as response:
            content = response.read()
        
        feed = feedparser.parse(content)
        
        for entry in feed.entries[:5]:
            if entry.link not in posted_links:
                title = entry.title
                prefix = await get_smart_prefix(title)
                
                # LMWM Style Crisp Formatting
                flash_msg = f"**{prefix}:**\n\n{title}\n\n@trade_with_PEACE1"

                try:
                    # Media support (Investing.com feeds aksar images dete hain)
                    media_url = None
                    if 'media_content' in entry:
                        media_url = entry.media_content[0]['url']
                    
                    if media_url:
                        await bot.send_photo(chat_id=CHANNEL_ID, photo=media_url, caption=flash_msg, parse_mode='Markdown')
                    else:
                        await bot.send_message(chat_id=CHANNEL_ID, text=flash_msg, parse_mode='Markdown', disable_web_page_preview=True)
                    
                    posted_links.add(entry.link)
                    print(f"✅ Success: {title[:40]}...")
                except Exception as e:
                    print(f"Telegram Send Error: {e}")

    except Exception as e:
        print(f"Fetch Error from {url}: {e}")

async def main():
    ssl_context = ssl._create_unverified_context()
    bot = telegram.Bot(token=BOT_TOKEN)
    posted_links = set()
    print("🚀 Pro-Market Bot Active (No-Bridge Mode)...")

    while True:
        for source in RSS_SOURCES:
            await fetch_and_post(bot, source, posted_links, ssl_context)
            await asyncio.sleep(10)
        
        await asyncio.sleep(180) # Har 3 minute mein check

if __name__ == "__main__":
    asyncio.run(main())
