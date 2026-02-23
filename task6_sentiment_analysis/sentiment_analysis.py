from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize
import pdfplumber

# Download punkt tokenizer
nltk.download('punkt')

#Load FinBERT from LOCAL folder
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="../finbert_model"
)

print("Model Loaded Successfully")


#Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text


#Function to analyze sentiment
def analyze_sentiment(text):
    sentences = sent_tokenize(text)

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            result = sentiment_pipeline(sentence)[0]

            print(f"Sentence: {sentence}")
            print(f"Sentiment: {result['label']}")
            print(f"Confidence: {result['score']:.4f}")
            print("-" * 60)


#MAIN
if __name__ == "__main__":
    pdf_file = "sample.pdf"   w
    text = extract_text_from_pdf(pdf_file)
    analyze_sentiment(text)