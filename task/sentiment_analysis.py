
def analyze_sentiment(text: str):

    positive_words = ["good", "great", "excellent", "profit", "growth", "increase"]
    negative_words = ["bad", "loss", "decline", "decrease", "poor"]

    text_lower = text.lower()

    pos_score = sum(word in text_lower for word in positive_words)
    neg_score = sum(word in text_lower for word in negative_words)

    if pos_score > neg_score:
        label = "positive"
    elif neg_score > pos_score:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "positive_score": pos_score,
        "negative_score": neg_score
    }