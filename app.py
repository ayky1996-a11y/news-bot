import os
import feedparser
import telegram
import asyncio
import urllib.request
import ssl

# Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trade_with_PEACE1"
# Yahoo Finance - Global Market, Crypto, and Economy impact news
RSS_URL = "https://finance.yahoo.com/news/rssindex"

async def main():
    # SSL context create karna
    ssl_context = ssl._create_unverified_context()
    bot = telegram.Bot(token=BOT_TOKEN)
    posted_links = set()
    print("🚀 Bot starting with Yahoo Finance Market Feed...")

    while True:
        try:
            print("🔍 Fetching latest market-moving news...")
            req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
            
            # Use urllib to fetch content first
            with urllib.request.urlopen(req, context=ssl_context) as response:
                content = response.read()
            
            feed = feedparser.parse(content)
            print(f"📊 Found {len(feed.entries)} entries.")

            # Filter keywords for market/politics impact
            keywords = ['stock', 'market', 'crypto', 'fed', 'inflation', 'gdp', 'economy', 'politics', 'election']

            for entry in feed.entries[:10]: # Check top 10
                if entry.link not in posted_links:
                    # Optional: Only send if keywords match (uncomment next line to filter)
                    # if any(word in entry.title.lower() for word in keywords):
                    
                    message = f"🚨 **MARKET IMPACT UPDATE**\n\n{entry.title}\n\n🔗 {entry.link}"
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
                    posted_links.add(entry.link)
                    print(f"✅ Sent: {entry.title}")
            
            print("⏳ Sleeping for 5 minutes...")
            await asyncio.sleep(300) 
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
