import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the required lexicon locally (Free/Open Source)
# This only happens once on the first run
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

# Initialize the VADER analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    """
    Analyzes text using VADER and returns a normalized score and label.
    
    Returns:
      sentiment_score: float (-1.0 to 1.0)
      sentiment_label: 'negative' | 'neutral' | 'positive'
    """
    if not text:
        return 0.0, "neutral"

    # scores is a dict: {'neg': 0.0, 'neu': 0.5, 'pos': 0.5, 'compound': 0.44}
    scores = analyzer.polarity_scores(text)
    
    # The compound score is the standard metric for overall sentiment
    compound_score = round(scores['compound'], 3)

    # Standard VADER thresholds:
    # Positive: >= 0.05
    # Neutral: between -0.05 and 0.05
    # Negative: <= -0.05
    if compound_score >= 0.05:
        label = "positive"
    elif compound_score <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return compound_score, label

if __name__ == "__main__":
    # Test cases to show off VADER's strengths
    test_titles = [
        "Massive layoffs hit tech giants as economy slows",
        "Startup raises $50M in successful Series B funding!",
        "Routine maintenance scheduled for Sunday"
    ]
    
    for title in test_titles:
        score, lbl = analyze_sentiment(title)
        print(f"Title: {title}\nScore: {score} | Label: {lbl}\n")