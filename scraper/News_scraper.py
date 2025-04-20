from newspaper import Article
import pandas as pd
import feedparser
from datetime import datetime
import os

# Fetch today's URLs from RSS feeds
def fetch_rss_urls(rss_url, max_articles=5):
    feed = feedparser.parse(rss_url)
    today = datetime.now().date()
    urls = []

    for entry in feed.entries:
        published = entry.get("published_parsed")
        if published:
            pub_date = datetime(*published[:6]).date()
            if pub_date == today:
                urls.append(entry.link)
        if len(urls) >= max_articles:
            break
    return urls

rss_urls = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml"
]

all_today_urls = []
for rss in rss_urls:
    all_today_urls.extend(fetch_rss_urls(rss))

# Scrape article text from today's URLs
def scrape_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return {
        "title": article.title,
        "text": article.text,
        "authors": article.authors,
        "published_date": article.publish_date,
        "url": url
    }

data = [scrape_article(url) for url in all_today_urls]
df = pd.DataFrame(data)

# Save with folder and date-based filename
today_str = datetime.now().strftime("%Y-%m-%d")
os.makedirs("Data", exist_ok=True)
df.to_csv(f"Data/news_data_{today_str}.csv", index=False)