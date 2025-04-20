# ================================
# Global News Scraper (Robust, RSS-Based)
# ================================

import os
import pandas as pd
from newspaper import Article
import feedparser
from datetime import datetime
import time
from tqdm import tqdm

# 🌐 Comprehensive Global RSS Feeds
rss_urls = [
    # International
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "http://feeds.reuters.com/Reuters/worldNews",
    "https://www.theguardian.com/world/rss",
    "https://www.cnn.com/rss/edition_world.rss",

    # US
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "http://feeds.foxnews.com/foxnews/latest",
    "https://feeds.npr.org/1004/rss.xml",

    # UK
    "https://feeds.skynews.com/feeds/rss/world.xml",

    # India
    "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    "https://www.hindustantimes.com/feeds/rss/world-news/rssfeed.xml",

    # Australia
    "https://www.abc.net.au/news/feed/51120/rss.xml",

    # China
    "http://www.chinadaily.com.cn/rss/world_rss.xml",

    # Africa
    "https://allafrica.com/tools/headlines/rdf/world/headlines.rdf",

    # Middle East
    "https://www.al-monitor.com/rss",

    # Europe
    "https://feeds.euronews.com/news/europe",

    # Southeast Asia
    "https://www.channelnewsasia.com/news/rss",

    # Business
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "http://feeds.reuters.com/reuters/businessNews"
]

# 📥 Step 1: Fetch today's URLs
def fetch_rss_urls(rss_url, max_articles=5):
    feed = feedparser.parse(rss_url)
    today = datetime.now().date()
    urls = set()

    for entry in feed.entries:
        pub_date = None
        try:
            published = entry.get("published_parsed") or entry.get("updated_parsed")
            if published:
                pub_date = datetime(*published[:6]).date()
        except:
            pass

        if pub_date == today or pub_date is None:
            urls.add(entry.link)

        if len(urls) >= max_articles:
            break
    return list(urls)

# 📄 Step 2: Scrape each article
def scrape_article(url, retries=3):
    for _ in range(retries):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return {
                "title": article.title,
                "text": article.text,
                "authors": article.authors,
                "published_date": article.publish_date,
                "url": url,
                "scraped_date": datetime.now().strftime("%Y-%m-%d")
            }
        except:
            time.sleep(1)
    return None

# 🔁 Process all feeds
all_today_urls = []
for rss in tqdm(rss_urls, desc="🔎 Fetching RSS Feeds"):
    all_today_urls.extend(fetch_rss_urls(rss, max_articles=5))

all_today_urls = list(set(all_today_urls))  # Deduplicate URLs

print(f"📰 Found {len(all_today_urls)} articles to scrape...")

# 🧹 Step 3: Scrape and clean articles
data = []
for url in tqdm(all_today_urls, desc="🧪 Scraping articles"):
    article_data = scrape_article(url)
    if article_data and article_data["text"]:  # Skip empty articles
        data.append(article_data)

df = pd.DataFrame(data)

# 💾 Step 4: Save with folder and date-based filename
os.makedirs("Data", exist_ok=True)
today_str = datetime.now().strftime("%Y-%m-%d")
df.to_csv(f"data/news_data_{today_str}.csv", index=False)
print(f"✅ Scraping complete. Saved {len(df)} articles to Data/news_data_{today_str}.csv")
