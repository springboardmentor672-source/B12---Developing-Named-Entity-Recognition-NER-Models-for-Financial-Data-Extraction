import nltk
from transformers import pipeline
import warnings
import torch

warnings.filterwarnings("ignore")

nltk.download('punkt_tab', quiet=True)

MODEL_NAME = "ProsusAI/finbert"
sentiment_pipeline = pipeline("sentiment-analysis", model=MODEL_NAME, tokenizer=MODEL_NAME)

# BERT max position embeddings is 512, but we need to account for special tokens
MAX_TOKENS = 500  # Leave room for [CLS] and [SEP] tokens


def chunk_text(text: str, max_tokens: int = MAX_TOKENS) -> list:
    """Split text into chunks that fit within token limit."""
    tokens = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for token in tokens:
        token_len = len(token)
        if current_length + token_len + 1 > max_tokens:  # +1 for space
            chunks.append(' '.join(current_chunk))
            current_chunk = [token]
            current_length = token_len
        else:
            current_chunk.append(token)
            current_length += token_len + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def analyze_sentiment(text: str) -> list:
    sentences = nltk.sent_tokenize(text)

    results = []
    for sentence in sentences:
        # Get token count for this sentence
        tokens = sentiment_pipeline.tokenizer.encode(sentence, add_special_tokens=True)

        if len(tokens) > MAX_TOKENS:
            # Chunk the sentence and analyze each part
            chunks = chunk_text(sentence, MAX_TOKENS)
            chunk_results = []
            for chunk in chunks:
                result = sentiment_pipeline(chunk)[0]
                chunk_results.append({
                    "label": result["label"],
                    "score": float(result["score"])
                })

            # Aggregate chunk results by averaging scores per label
            label_scores = {}
            for cr in chunk_results:
                label = cr["label"]
                if label not in label_scores:
                    label_scores[label] = []
                label_scores[label].append(cr["score"])

            # Pick the label with highest average score
            avg_scores = {label: sum(scores) / len(scores) for label, scores in label_scores.items()}
            best_label = max(avg_scores, key=avg_scores.get)
            best_score = avg_scores[best_label]

            results.append({
                "sentence": sentence[:200] + "..." if len(sentence) > 200 else sentence,
                "label": best_label,
                "score": best_score,
                "chunked": True
            })
        else:
            result = sentiment_pipeline(sentence)[0]
            results.append({
                "sentence": sentence,
                "label": result["label"],
                "score": float(result["score"]),
                "chunked": False
            })

    return results

if __name__ == "__main__":
    sample_text = """Apple Inc. reported a quarterly revenue of $117.9 billion, up 11% from the previous year. The company's stock price surged to $150 per share following the announcement. Meanwhile, Tesla's market capitalization reached $600 billion after unveiling its new electric vehicle model. Investors are closely watching the Federal Reserve's interest rate decisions, which could impact bond yields and inflation rates. In other news, JPMorgan Chase & Co. acquired a fintech startup for $1.2 billion to enhance its digital banking services."""
    
    sentiments = analyze_sentiment(sample_text)
    for sentiment in sentiments:
        print(f"Sentence: {sentiment['sentence']}")
        print(f"Label: {sentiment['label']}, Score: {sentiment['score']:.4f}")
        print("-" * 50)