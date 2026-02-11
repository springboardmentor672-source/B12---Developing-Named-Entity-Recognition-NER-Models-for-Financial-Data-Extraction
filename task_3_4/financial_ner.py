import requests
import re
import os
import time

class FinancialNER:
    def __init__(self, api_token):
        self.api_url = "https://router.huggingface.co/hf-inference/models/dslim/bert-base-NER"
        self.headers = {"Authorization": f"Bearer {api_token}"}
        
        self.patterns = {
            "FISCAL_PERIOD": r"\b(Q[1-4]|First Quarter|Second Quarter|Third Quarter|Fourth Quarter|Fiscal Year \d{4})\b",
            "MONEY": r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d+)?\s?(?:billion|million|trillion|B|M)?",
            "PERCENT": r"\d+(?:\.\d+)?\s?%",
            "METRIC": r"\b(Revenue|Net Income|Operating Income|EPS|Earnings Per Share|Free Cash Flow|Dividend)\b"
        }

    def _query_hf(self, text_chunk):
        """Sends a small chunk of text to Hugging Face."""
        try:
            payload = {"inputs": text_chunk, "parameters": {"aggregation_strategy": "simple"}}
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                print(f"   ⚠️ API Error {response.status_code}: {response.text[:100]}...")
                return []
            return response.json()
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
            return []

    def analyze(self, text):
        print(f"   > Starting Analysis on {len(text)} characters...")
        
        extracted = {
            "ORG": [], "PER": [], "LOC": [], 
            "MONEY": [], "METRIC": [], "PERIOD": [], "MISC": []
        }

        # --- STEP 1: AI Analysis (With Chunking) ---
        # We split text into chunks of 1000 characters to respect API limits
        chunk_size = 1000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        print(f"   > Split document into {len(chunks)} chunks for AI processing.")

        for i, chunk in enumerate(chunks):
            print(f"     Processing Chunk {i+1}/{len(chunks)}...", end="\r")
            
            ai_results = self._query_hf(chunk)
            
            if isinstance(ai_results, list):
                for item in ai_results:
                    if not isinstance(item, dict): continue
                    
                    # Only keep high confidence (>80%) entities
                    if item.get('score', 0) > 0.80:
                        group = item.get('entity_group')
                        word = item.get('word')
                        
                        if group in extracted:
                            extracted[group].append(word)
            
            # Sleep briefly to be nice to the free API
            time.sleep(0.5)

        print("\n   > AI Analysis Complete.")

        # --- STEP 2: Regex Analysis (Fast) ---
        for key, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            target_key = "MISC"
            if key == "FISCAL_PERIOD": target_key = "PERIOD"
            elif key == "MONEY": target_key = "MONEY"
            elif key == "METRIC": target_key = "METRIC"
            
            extracted[target_key].extend(matches)

        # --- STEP 3: Clean and Deduplicate ---
        for key in extracted:
            # Clean up artifacts (like "Go ##ogle" -> "Google")
            clean_list = [item.replace("##", "") for item in extracted[key]]
            extracted[key] = sorted(list(set(clean_list)))
            
        return extracted

def save_to_markdown(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🏦 Financial Entity Extraction Report\n")
        f.write(f"**Source:** Automated Analysis\n\n")
        f.write("---\n\n")
        
        headers = {
            "ORG": "🏢 Companies & Organizations",
            "PER": "👤 Key Executives & People",
            "LOC": "🌍 Locations & Regions",
            "MONEY": "💰 Financial Figures",
            "METRIC": "📊 Key Metrics Detected",
            "PERIOD": "📅 Fiscal Periods",
            "MISC": "📎 Other Details (Percentages)"
        }
        
        for key, title in headers.items():
            items = data.get(key, [])
            if items:
                f.write(f"### {title}\n")
                for item in items:
                    f.write(f"- {item}\n")
                f.write("\n")
            else:
                f.write(f"### {title}\n")
                f.write("*(No entities detected)*\n\n")

    print(f"✅ Report saved to: {output_path}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. YOUR TOKEN
    MY_TOKEN = "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" 
    
    # 2. Files
    input_path = os.path.join("output", "earnings.txt")
    output_path = os.path.join("output", "financial_entities.md")
    
    # 3. Load & Clean Text
    if os.path.exists(input_path):
        with open(input_path, "r", encoding="utf-8") as f:
            text_content = f.read()
            # BASIC CLEANUP: Remove excessive newlines that confuse AI
            text_content = text_content.replace("\n", " ").replace("  ", " ")
            print(f"📂 Loaded text from: {input_path}")
    else:
        text_content = "Google Cloud (ORG) reported Q3 revenue (METRIC) of $10.2 billion. Sundar Pichai (PER) is the CEO."
        print("⚠️ Warning: earnings.txt not found.")

    # 4. Run
    ner = FinancialNER(MY_TOKEN)
    results = ner.analyze(text_content)

    # 5. Save
    save_to_markdown(results, output_path)