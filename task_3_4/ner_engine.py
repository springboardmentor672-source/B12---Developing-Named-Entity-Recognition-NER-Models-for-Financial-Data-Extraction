import requests
import json
import os

class HuggingFaceNER:
    def __init__(self, api_token):
        # CORRECT URL for the new Hugging Face Router
        self.api_url = "https://router.huggingface.co/hf-inference/models/dslim/bert-base-NER"
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def query(self, text):
        """Sends text to Hugging Face and returns entities."""
        payload = {
            "inputs": text,
            "parameters": {"aggregation_strategy": "simple"}
        }
        
        try:
            # Send the request
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            # Error Handling
            if response.status_code != 200:
                print(f"⚠️ API Error (Status {response.status_code}):")
                print(f"   Response: {response.text[:200]}...") 
                return []
            
            return response.json()
        
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return []

    def analyze(self, text):
        # Hugging Face has a limit on text length (usually ~512 words).
        # We take the first 2000 characters for this demo to avoid errors.
        truncated_text = text[:2000] 
        
        print(f"   > Sending {len(truncated_text)} chars to Hugging Face Cloud...")
        results = self.query(truncated_text)
        
        entities = {"ORG": [], "LOC": [], "PER": [], "MISC": []}
        
        if isinstance(results, list):
            for item in results:
                if not isinstance(item, dict): continue
                
                label = item.get('entity_group')
                word = item.get('word')
                score = item.get('score')
                
                # Only keep entities where the AI is >80% confident
                if score and score > 0.80: 
                    if label in entities:
                        entities[label].append(word)

        # Remove duplicates and sort
        for key in entities:
            entities[key] = sorted(list(set(entities[key])))
            
        return entities

def load_text_from_file(filename):
    """Reads content from a file safely."""
    if not os.path.exists(filename):
        print(f"❌ Error: The file '{filename}' was not found.")
        return None
    
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. YOUR TOKEN (Make sure this is correct!)
    MY_TOKEN = "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" 
    
    # 2. Define the path to your earnings.txt
    # We assume 'output' folder is in the same directory as this script
    input_file = os.path.join("output", "earnings.txt")

    print(f"📂 Reading text from: {input_file}")
    text_content = load_text_from_file(input_file)

    if text_content:
        # 3. Initialize Engine & Run
        ner = HuggingFaceNER(MY_TOKEN)
        
        print("\n--- 🤖 STARTING HUGGING FACE ANALYSIS ---")
        analysis = ner.analyze(text_content)
        
        # 4. Print the Clean List
        print("\n" + "="*40)
        print("      FINANCIAL ENTITY REPORT      ")
        print("="*40)
        
        for category, items in analysis.items():
            print(f"\n📁 {category} ({len(items)} found):")
            if not items:
                print("   (None)")
            for item in items:
                print(f"   • {item}")
                
        print("\n" + "="*40)