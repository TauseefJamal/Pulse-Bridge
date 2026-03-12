import requests
from database import get_connection, create_tables
from utils.sentiment import analyze_sentiment
from utils.classifier import classify_news
from utils.anomaly import check_for_anomaly

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def fetch_top_story_ids(limit=30):
    try:
        response = requests.get(HN_TOP_STORIES_URL, timeout=10)
        response.raise_for_status()
        return response.json()[:limit]
    except Exception as e:
        print(f"Error fetching IDs: {e}")
        return []

def fetch_story(story_id):
    try:
        response = requests.get(HN_ITEM_URL.format(story_id), timeout=10)
        return response.json()
    except:
        return None

def bulk_save_news(news_list):
    """Saves multiple news items in one transaction for speed."""
    if not news_list:
        return
        
    with get_connection() as conn:
        cursor = conn.cursor()
        # INSERT OR IGNORE works with our UNIQUE title constraint
        cursor.executemany("""
            INSERT OR IGNORE INTO news (title, source, category, sentiment_score, sentiment_label)
            VALUES (?, ?, ?, ?, ?)
        """, news_list)
        conn.commit()

def save_alert(alert_type, message):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alerts (alert_type, message) VALUES (?, ?)",
            (alert_type, message),
        )
        conn.commit()

def process_news():
    create_tables()
    story_ids = fetch_top_story_ids()
    news_to_save = []

    for story_id in story_ids:
        story = fetch_story(story_id)
        if not story or not story.get("title"):
            continue

        title = story.get("title")
        sentiment_score, sentiment_label = analyze_sentiment(title)
        category = classify_news(title)

        news_to_save.append((title, "Hacker News", category, sentiment_score, sentiment_label))

    bulk_save_news(news_to_save)
    # Check for spikes after adding new data
    check_for_anomaly(save_alert)

if __name__ == "__main__":
    process_news()