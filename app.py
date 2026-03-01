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
RSS_URL = "https://finance.yahoo.com/news/rssindex"

# --- Keywords for Market & Geopolitical Impact ---
KEYWORDS = [
    # Geopolitical (Impacts Gold & Crude Oil)
    'war', 'iran', 'israel', 'conflict', 'sanctions', 'crude', 'oil', 'geopolitical', 'opec', 'red sea',
    # Macroeconomics (Impacts Stocks & Nifty)
    'fed', 'fomc', 'inflation', 'cpi', 'interest rate', 'gdp', 'rbi', 'recession', 'dollar index', 'dxy', 'yield',
    # Crypto Market
    'bitcoin', 'btc', 'crypto', 'eth', 'ethereum', 'sec', 'etf', 'binance', 'halving',
    # Stock Market Specific
    'stock', 'market', 'trade', 'nifty', 'sensex', 'earnings', 'ipo', 'sebi', 'fii', 'dii'
]

async def main():
    ssl_context = ssl._create_unverified_context()
    bot = telegram.Bot(token=BOT_TOKEN)
    posted_links = set()
    print("🚀 Bot starting with advanced market & political filters...")

    while True:
        try:
            print("🔍 Scanning for market-moving news...")
            req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ssl_context) as response:
                content = response.read()
            
            feed = feedparser.parse(content)
            
            for entry in feed.entries[:20]: # Zyada entries scan kar rahe hain taaki keywords mil sakein
                if entry.link not in posted_links:
                    title = entry.title
                    summary = entry.get('summary', '') or entry.get('description', '')
                    
                    # Keywords check (Filter logic)
                    if any(word in title.lower() for word in KEYWORDS) or any(word in summary.lower() for word in KEYWORDS):
                        
                        # Summary cleanup (HTML hatana aur chota karna)
                        clean_summary = re.sub('<[^<]+?>', '', summary)
                        short_summary = clean_summary[:250] + "..." if len(clean_summary) > 250 else clean_summary

                        message = (
                            f"🚨 **MARKET IMPACT ALERT**\n\n"
                            f"📌 **Title:** {title}\n\n"
                            f"📝 **Summary:** {short_summary}\n\n"
                            f"🔗 [Read Full Analysis]({entry.link})"
                        )
                        
                        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
                        posted_links.add(entry.link)
                        print(f"✅ Sent: {title}")
            
            print("⏳ Monitoring... Next check in 5 minutes.")
            await asyncio.sleep(300) 
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
