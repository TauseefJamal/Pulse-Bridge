from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

# Import your optimized local modules
from database import create_tables, get_connection
from fetcher import process_news

app = FastAPI(title="Pulse-Bridge")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    """Ensure database tables and WAL mode are initialized on launch."""
    create_tables()


@app.get("/")
def dashboard(request: Request):
    """Renders the main dashboard interface."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/api/refresh")
async def trigger_refresh(background_tasks: BackgroundTasks):
    """
    Triggers the news scraper in the background.
    Allows the UI to return a 200 OK immediately while the work happens.
    """
    background_tasks.add_task(process_news)
    return {"status": "success", "message": "Scraper started in background"}


@app.get("/api/latest")
def get_latest_news(limit: int = 20):
    """Fetches the most recent headlines using a safe connection context."""
    with get_connection() as conn:
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

    return [
        {
            "title": row["title"],
            "category": row["category"],
            "sentiment_score": row["sentiment_score"],
            "sentiment_label": row["sentiment_label"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


@app.get("/api/summary")
def get_summary():
    """Calculates overall sentiment and category distribution."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Aggregate stats with null handling for first-run empty databases
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_news,
                AVG(sentiment_score) as avg_sentiment
            FROM news
            """
        )
        summary = cursor.fetchone()

        # Count distribution per category
        cursor.execute(
            """
            SELECT category, COUNT(*) as count
            FROM news
            GROUP BY category
            """
        )
        categories = cursor.fetchall()

    return {
        "total_news": summary["total_news"] if summary["total_news"] else 0,
        "avg_sentiment": round(summary["avg_sentiment"], 3) if summary["avg_sentiment"] else 0,
        "categories": [
            {"category": row["category"], "count": row["count"]}
            for row in categories
        ],
    }


@app.get("/api/alerts")
def get_active_alerts():
    """Retrieves all currently active system alerts (volume spikes/sentiment drops)."""
    with get_connection() as conn:
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

    return [
        {
            "id": row["id"],
            "type": row["alert_type"],
            "message": row["message"],
            "created_at": row["created_at"],
        }
        for row in alerts
    ]


@app.post("/api/alerts/resolve/{alert_id}")
def resolve_alert(alert_id: int):
    """Marks a specific alert as resolved."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alerts SET is_active = 0 WHERE id = ?",
            (alert_id,)
        )
        conn.commit()
    return {"status": "success", "message": f"Alert {alert_id} resolved"}