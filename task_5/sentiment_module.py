import requests
import re
import time
import json
import sys
import os

class FinancialSentiment:
    def __init__(self, api_token):
        # Using the specialized Financial BERT model
        self.api_url = "https://router.huggingface.co/hf-inference/models/ProsusAI/finbert"
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def split_sentences(self, text):
        """Splits text into sentences."""
        text = text.replace('\n', ' ').replace('  ', ' ')
        # Regex: Period/Question mark + Space + Capital Letter
        pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if len(s) > 15]

    def query_api(self, text):
        """Sends a SINGLE sentence to the API."""
        retries = 0
        while retries < 3:
            try:
                response = requests.post(self.api_url, headers=self.headers, json={"inputs": text})
                
                if response.status_code == 200:
                    return response.json()
                
                # Handle Model Loading (503)
                try:
                    err = response.json()
                except:
                    err = {}
                
                if "estimated_time" in err:
                    wait = err['estimated_time']
                    print(f"     ⏳ Model loading... waiting {wait:.1f}s")
                    time.sleep(wait + 1)
                    retries += 1
                    continue
                
                return []
            except Exception as e:
                print(f"     ❌ Connection Error: {e}")
                return []
        return []

    def analyze(self, text):
        print("   > 1. Splitting document into sentences...")
        sentences = self.split_sentences(text)
        print(f"   > Found {len(sentences)} valid sentences.")
        
        results = []
        print(f"   > 2. Analyzing sentiment (One by One)...")

        for i, sentence in enumerate(sentences):
            print(f"     Processing {i+1}/{len(sentences)}...", end="\r")
            data = self.query_api(sentence)
            
            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                # Handle different API response formats
                if isinstance(first_item, list):
                    top = max(first_item, key=lambda x: x['score'])
                    label, score = top['label'], top['score']
                elif isinstance(first_item, dict):
                    if 'label' in first_item:
                         top = max(data, key=lambda x: x['score'])
                         label, score = top['label'], top['score']
                    else:
                        label, score = "unknown", 0.0

                results.append({
                    "sentence": sentence,
                    "label": label,
                    "score": score
                })
            time.sleep(0.3) # Be nice to the API

        print(f"\n   > Analysis Complete. Processed {len(results)} sentences.")
        return results

    def save_report(self, results, filename):
        positive = [r for r in results if r['label'] == 'positive']
        negative = [r for r in results if r['label'] == 'negative']
        neutral =  [r for r in results if r['label'] == 'neutral']
        
        # --- CALCULATE OVERALL SENTIMENT ---
        total = len(results)
        if total > 0:
            # We ignore Neutral for the "Sentiment Direction"
            # If Positives > Negatives -> Bullish
            if len(positive) > len(negative):
                verdict = "🟢 BULLISH (Optimistic)"
                description = "The document contains more positive financial signals than negative ones."
            elif len(negative) > len(positive):
                verdict = "🔴 BEARISH (Pessimistic)"
                description = "Negative risks and concerns outweigh the positive growth indicators."
            else:
                verdict = "⚪ NEUTRAL (Balanced)"
                description = "The positive and negative signals are roughly equal."
        else:
            verdict = "⚪ NO DATA"
            description = "No valid sentences were analyzed."

        with open(filename, "w", encoding="utf-8") as f:
            f.write("# 📈 Financial Sentiment Analysis Report\n")
            f.write(f"**Overall Verdict:** {verdict}\n\n")
            f.write(f"*{description}*\n\n")
            f.write("---\n")
            
            f.write("### 📊 Executive Summary\n")
            f.write(f"- **Total Sentences:** {len(results)}\n")
            f.write(f"- 🟢 **Positive:** {len(positive)}\n")
            f.write(f"- 🔴 **Negative:** {len(negative)}\n")
            f.write(f"- ⚪ **Neutral:** {len(neutral)}\n\n")
            f.write("---\n")

            # Helper function to write sections uniformly WITH SCORES
            def write_section(title, items):
                f.write(f"### {title}\n")
                # Sort by highest confidence
                sorted_items = sorted(items, key=lambda x: x['score'], reverse=True)
                for item in sorted_items:
                    score_pct = item['score'] * 100
                    # Format: "- **95.2%** Confidence: *The sentence text...*"
                    f.write(f"- **{score_pct:.1f}%** Confidence: *\"{item['sentence']}\"*\n")
                f.write("\n")

            if positive: write_section("🟢 Positive Highlights", positive)
            if negative: write_section("🔴 Negative Risks", negative)
            if neutral: write_section("⚪ Neutral Statements", neutral)

        print(f"✅ Report saved to: {filename}")

# --- STANDALONE RUNNER ---
if __name__ == "__main__":
    # 1. PASTE YOUR TOKEN HERE
    MY_TOKEN = "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" 
    
    # 2. Define File Paths (We look for the .txt file directly)
    input_path = os.path.join("output", "earnings.txt")
    output_path = os.path.join("output", "earnings_sentiment.md")

    # 3. Check if the text file exists
    if os.path.exists(input_path):
        print(f"📂 Found data file: {input_path}")
        print("🚀 Starting Sentiment Analysis...")
        
        # Read the file
        with open(input_path, "r", encoding="utf-8") as f:
            text_content = f.read()
            
        # Run Analysis
        analyzer = FinancialSentiment(MY_TOKEN)
        data = analyzer.analyze(text_content)
        
        # Save Report
        analyzer.save_report(data, output_path)
    else:
        print(f"❌ Error: Could not find '{input_path}'")
        print("   Make sure you have run the conversion step at least once.")
        print("   (Or check that 'earnings.txt' is inside the 'output' folder)")