import sys
import os
from pdf_processor import convert_pdf_to_text
from sentiment_module import analyze_sentiment, generate_structured_report


def main():

    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf_file>")
        return

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print("Error: PDF file not found.")
        return

    print("Converting PDF to text...")
    text_content = convert_pdf_to_text(pdf_path)

    if len(text_content) == 0:
        print("Error: Extracted text is empty.")
        return

    print("Running Financial Sentiment Analysis...")
    results = analyze_sentiment(text_content)

    report = generate_structured_report(results)

    print("\n================ FINANCIAL SENTIMENT REPORT ================")

    print("\n📊 Overall Sentiment Distribution")
    print(report["summary"])

    print("\n⚠ High Risk Statements")
    for item in report["high_risk_statements"]:
        print(f"- {item['sentence']} ({item['confidence']})")

    print("\n📈 Positive Indicators")
    for item in report["positive_indicators"]:
        print(f"- {item['sentence']} ({item['confidence']})")

    print("\n=============================================================")


if __name__ == "__main__":
    main()