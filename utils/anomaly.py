from datetime import datetime, timedelta
from database import get_connection

WINDOW_MINUTES = 30
SPIKE_THRESHOLD = 5   
SENTIMENT_DROP_THRESHOLD = -0.4 # Alert if sentiment turns very negative

def check_for_anomaly(save_alert_callback):
    """
    Checks for sudden spikes in volume OR a sharp drop in sentiment.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        window_start = datetime.utcnow() - timedelta(minutes=WINDOW_MINUTES)

        cursor.execute(
            """
            SELECT category, COUNT(*) as count, AVG(sentiment_score) as avg_sent
            FROM news
            WHERE created_at >= ?
            GROUP BY category
            """,
            (window_start,),
        )
        rows = cursor.fetchall()

    for row in rows:
        category = row["category"]
        count = row["count"]
        avg_sent = row["avg_sent"]

        # 1. Volume Spike Detection
        if count >= SPIKE_THRESHOLD:
            message = f"🚨 Volume Spike: {count} '{category}' stories in {WINDOW_MINUTES}m."
            save_alert_callback("spike", message)

        # 2. Negative Sentiment Alert (New!)
        if avg_sent <= SENTIMENT_DROP_THRESHOLD:
            message = f"📉 Sentiment Drop: '{category}' news is trending negative ({avg_sent})."
            save_alert_callback("sentiment_drop", message)