CATEGORIES = {
    "layoffs": ["layoff", "laid off", "job cut", "firing", "cuts"],
    "funding": ["funding", "raises", "raised", "series", "investment", "vc"],
    "security": ["breach", "hack", "leak", "attack", "vulnerability"],
    "product": ["launch", "released", "update", "version", "rollout"],
    "regulation": ["law", "regulation", "policy", "ban", "government"],
    "outage": ["down", "outage", "incident", "disruption", "offline"],
}


def classify_news(title: str) -> str:
    """
    Returns a category string based on keyword matching.
    """
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for word in keywords:
            if word in title_lower:
                return category

    return "general"
