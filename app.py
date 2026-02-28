import feedparser
import telegram
import time
import os

BOT_TOKEN = os.getenv("8788108827:AAGIXJtvH1VbI2BOON7aO1fHzev-hsalHHE")
CHANNEL_ID = "@trade_with_PEACE1"

bot = telegram.Bot(token=BOT_TOKEN)

RSS_URL = "https://feeds.reuters.com/reuters/worldNews"

posted_links = set()

while True:
    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries[:3]:
        if entry.link not in posted_links:
            message = f"""🚨 BREAKING NEWS

{entry.title}

📝 {entry.summary[:180]}...

#GlobalNews #BreakingNews
"""
            bot.send_message(chat_id=CHANNEL_ID, text=message)
            posted_links.add(entry.link)

    time.sleep(600)
