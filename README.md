# 🫀 Pulse Bridge

**A real-time news signal monitor that tells you what's happening in tech — and how the internet feels about it.**

Pulse Bridge scrapes the top stories from Hacker News, runs them through an NLP sentiment pipeline, categorizes them automatically, and surfaces everything on a live dashboard. If something unusual is happening — a topic suddenly blowing up, or the news turning sharply negative — it fires an alert so you don't miss it.

---

## 🖥️ What It Looks Like

A clean, minimal dashboard with:
- Live headline feed with sentiment scores
- Category badges (funding, layoffs, security, etc.)
- Overall sentiment average across all stories
- Active alert banner for anomalies — dismissable with one click
- Dark / Light theme toggle that remembers your preference

---

## ⚙️ How It Works

1. You hit **Refresh** on the dashboard (or it auto-polls every 60 seconds)
2. The app fetches the top 30 stories from the Hacker News API in the background
3. Each headline gets:
   - A **sentiment score** from -1.0 (very negative) to +1.0 (very positive) using VADER
   - A **category label** based on keyword matching (layoffs, funding, security, product, regulation, outage, or general)
4. Everything gets saved into a local SQLite database (WAL mode, so reads and writes don't block each other)
5. The anomaly engine checks if any category has spiked in volume or gone sharply negative — and raises an alert if so

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI (Python) |
| Database | SQLite with WAL mode |
| Sentiment | VADER via NLTK |
| Frontend | Jinja2 + Vanilla JS |
| News Source | Hacker News Firebase API |

---

## 🚀 Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/TauseefJamal/Pulse-Bridge.git
cd Pulse-Bridge
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# or
source .venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

**3. Run the app**
```bash
uvicorn main:app --reload
```

**4. Open your browser**
```
http://localhost:8000
```

Hit **Refresh** on the dashboard to pull in the first batch of stories.

---

## 📁 Project Structure

```
PulseBridge/
│
├── main.py              # FastAPI app — all API routes
├── database.py          # SQLite connection + table setup
├── fetcher.py           # Hacker News scraper + bulk save logic
├── models.py            # DB query helpers
│
├── utils/
│   ├── sentiment.py     # VADER sentiment analysis
│   ├── classifier.py    # Keyword-based category classifier
│   └── anomaly.py       # Volume spike + sentiment drop detection
│
├── templates/
│   └── index.html       # Dashboard UI (HTML + CSS + JS)
│
├── data/
│   └── pulsebridge.db   # Local SQLite database (auto-created)
│
└── requirements.txt
```

---

## 🚨 Alert System

Pulse Bridge watches for two types of anomalies in a rolling 30-minute window:

- **Volume Spike** — 5 or more stories in the same category within 30 minutes
- **Sentiment Drop** — average sentiment for a category falls below -0.4

When either trigger is triggered, an alert banner appears at the top of the dashboard. You can dismiss it once you've seen it.

---

## 👤 Author

**Md Tauseef Jamal**  
[GitHub](https://github.com/TauseefJamal) · [Portfolio](https://tauseefjamal.github.io/Portfolio)
