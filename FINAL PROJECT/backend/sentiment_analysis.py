import nltk
from transformers import pipeline, AutoTokenizer
import warnings

warnings.filterwarnings("ignore")

# Download tokenizer data
nltk.download('punkt', quiet=True)

# Load FinBERT model
MODEL_NAME = "ProsusAI/finbert"

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME
)

# Load tokenizer separately for chunking
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# BERT max tokens limit (keep buffer <512)
MAX_TOKENS = 500


def chunk_text(text: str, max_tokens: int = MAX_TOKENS) -> list:
    """
    Split text into token-safe chunks using tokenizer.
    Ensures no chunk exceeds model token limit.
    """
    tokens = tokenizer.encode(text, add_special_tokens=False)

    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks


def analyze_sentiment(text: str) -> list:
    """
    Analyze sentiment safely for large text using chunking.
    Returns sentence-wise sentiment with aggregation.
    """
    sentences = nltk.sent_tokenize(text)

    results = []

    for sentence in sentences:
        chunks = chunk_text(sentence, MAX_TOKENS)

        try:
            # Process all chunks together (faster)
            predictions = sentiment_pipeline(chunks)
        except Exception as e:
            print("Chunk error:", e)
            continue

        # Aggregate chunk results
        label_scores = {}

        for pred in predictions:
            label = pred["label"]
            score = float(pred["score"])
            label_scores.setdefault(label, []).append(score)

        if not label_scores:
            continue

        # Average scores per label
        avg_scores = {
            label: sum(scores) / len(scores)
            for label, scores in label_scores.items()
        }

        best_label = max(avg_scores, key=avg_scores.get)

        results.append({
            "sentence": sentence[:200] + "..." if len(sentence) > 200 else sentence,
            "label": best_label,
            "score": round(avg_scores[best_label], 4),
            "chunked": len(chunks) > 1
        })

    return results


# 🔥 Optional Test Block
if __name__ == "__main__":
    sample_text = """Apple Inc. reported a quarterly revenue of $117.9 billion, up 11% from the previous year. 
    The company's stock price surged to $150 per share following the announcement. 
    Meanwhile, Tesla's market capitalization reached $600 billion after unveiling its new electric vehicle model. 
    Investors are closely watching the Federal Reserve's interest rate decisions, which could impact bond yields and inflation rates."""

    sentiments = analyze_sentiment(sample_text)

    for sentiment in sentiments:
        print(f"Sentence: {sentiment['sentence']}")
        print(f"Label: {sentiment['label']}, Score: {sentiment['score']}")
        print(f"Chunked: {sentiment['chunked']}")
        print("-" * 50)