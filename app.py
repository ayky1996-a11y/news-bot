import os
import feedparser
import telegram
import asyncio
import urllib.request
import ssl

# Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trade_with_PEACE1"
RSS_URL = "https://www.moneycontrol.com/rss/business.xml"

async def main():
    # SSL context create karna taaki connection fail na ho
    context = ssl._create_unverified_context()
    bot = telegram.Bot(token=BOT_TOKEN)
    posted_links = set()
    print("🚀 Bot starting with Moneycontrol feed...")

    while True:
        try:
            print("🔍 Fetching latest news...")
            req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=context) as response:
                content = response.read()
            
            feed = feedparser.parse(content)
            print(f"📊 Found {len(feed.entries)} entries.")

            for entry in feed.entries[:5]:
                if entry.link not in posted_links:
                    # News formatting
                    message = f"🚨 **MARKET UPDATE**\n\n{entry.title}\n\n🔗 {entry.link}"
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
