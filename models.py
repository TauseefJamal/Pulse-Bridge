from database import get_connection


# ---------- NEWS QUERIES ----------

def news_exists(title: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM news WHERE title = ? LIMIT 1",
        (title,)
    )

    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def insert_news(title, source, category, sentiment_score, sentiment_label):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO news (title, source, category, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, source, category, sentiment_score, sentiment_label)
    )

    conn.commit()
    conn.close()


def get_latest_news(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title, category, sentiment_score, sentiment_label, created_at
        FROM news
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_news_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) AS total, AVG(sentiment_score) AS avg_sentiment FROM news"
    )
    summary = cursor.fetchone()

    cursor.execute(
        "SELECT category, COUNT(*) AS count FROM news GROUP BY category"
    )
    categories = cursor.fetchall()

    conn.close()
    return summary, categories


# ---------- ALERT QUERIES ----------

def insert_alert(alert_type, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO alerts (alert_type, message)
        VALUES (?, ?)
        """,
        (alert_type, message)
    )

    conn.commit()
    conn.close()


def get_active_alerts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, alert_type, message, created_at
        FROM alerts
        WHERE is_active = 1
        ORDER BY created_at DESC
        """
    )

    alerts = cursor.fetchall()
    conn.close()
    return alerts


def resolve_alert(alert_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE alerts SET is_active = 0 WHERE id = ?",
        (alert_id,)
    )

    conn.commit()
    conn.close()
