import feedparser
from datetime import datetime
import time

# RSS Feeds Configuration
FEEDS = {
    "world": [
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "http://rss.cnn.com/rss/edition_world.rss",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html" # Top News
    ],
    "malaysia": [
        "https://www.thestar.com.my/rss/news/nation",
        "https://www.thestar.com.my/rss/business/business-news",
        "https://www.malaymail.com/feed/rss/malaysia",
        "https://www.bernama.com/en/rss/news.php?cat=general"
    ]
}

# Keywords for scoring importance
IMPORTANT_KEYWORDS = {
    "high": [
        "market", "economy", "crisis", "surge", "crash", "policy", "ban", 
        "investment", "trade", "inflation", "gdp", "tax", "regulation", 
        "merger", "acquisition", "war", "conflict", "election", "scandal",
        "profit", "loss", "record", "bank", "interest rate", "dividend"
    ],
    "medium": [
        "launch", "announce", "update", "report", "growth", "decline", 
        "forecast", "trend", "sector", "industry", "technology", "development"
    ]
}

def calculate_score(entry):
    """
    Calculates an importance score for a news entry based on keywords.
    """
    score = 0
    text = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
    
    # Keyword scoring
    for keyword in IMPORTANT_KEYWORDS["high"]:
        if keyword in text:
            score += 10
    
    for keyword in IMPORTANT_KEYWORDS["medium"]:
        if keyword in text:
            score += 5
            
    # Recency bonus (if published today) - simplistic approach
    # In a real app, we'd parse the 'published_parsed' struct_time accurately
    # For now, just a small flat bonus if we can parse it and it's recent
    if entry.get("published_parsed"):
        published_ts = time.mktime(entry.published_parsed)
        current_ts = time.time()
        # Bonus for news in last 24 hours
        if (current_ts - published_ts) < 86400:
            score += 5

    return score

def fetch_news(category="world", limit=5):
    """
    Fetches news from the defined feeds for the given category,
    scores them, and returns the top `limit` items.
    """
    if category not in FEEDS:
        return []

    all_entries = []
    seen_titles = set()

    print(f"Fetching {category} news...")
    
    for url in FEEDS[category]:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                
                # Deduplication
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                
                # Calculate Score
                score = calculate_score(entry)
                
                # Format entry
                news_item = {
                    "title": title,
                    "link": entry.get("link", "#"),
                    "summary": entry.get("summary", ""),
                    "source": feed.feed.get("title", "Unknown Source"),
                    "published": entry.get("published", "Unknown Date"),
                    "score": score
                }
                all_entries.append(news_item)
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # Sort by score (descending)
    sorted_news = sorted(all_entries, key=lambda x: x["score"], reverse=True)
    
    return sorted_news[:limit]

if __name__ == "__main__":
    # Test run
    print("--- TOP 5 WORLD NEWS ---")
    world_news = fetch_news("world", 5)
    for n in world_news:
        print(f"[{n['score']}] {n['title']} ({n['source']})")
    
    print("\n--- TOP 5 MALAYSIA NEWS ---")
    my_news = fetch_news("malaysia", 5)
    for n in my_news:
        print(f"[{n['score']}] {n['title']} ({n['source']})")
