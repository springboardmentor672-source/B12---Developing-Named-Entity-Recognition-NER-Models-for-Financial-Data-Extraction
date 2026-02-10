import requests
import json
import time

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
            
            # Error Handling: If the server returns a non-200 code
            if response.status_code != 200:
                print(f"⚠️ API Error (Status {response.status_code}):")
                print(f"   Response: {response.text[:200]}...") # Print first 200 chars of error
                return []
            
            return response.json()
        
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return []

    def analyze(self, text):
        print(f"   > Sending {len(text)} chars to Hugging Face Cloud...")
        results = self.query(text)
        
        # Initialize empty lists for our categories
        entities = {"ORG": [], "LOC": [], "PER": [], "MISC": []}
        
        # Process the results if they are a list (which means success)
        if isinstance(results, list):
            for item in results:
                # Skip if item is not a dictionary (rare error case)
                if not isinstance(item, dict): continue
                
                label = item.get('entity_group') # e.g., 'ORG'
                word = item.get('word')
                score = item.get('score')
                
                # Only keep entities where the AI is >80% confident
                if score and score > 0.80: 
                    if label in entities:
                        entities[label].append(word)

        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
            
        return entities

# --- TEST RUN ---
if __name__ == "__main__":
    # Your Token is already set here
    MY_TOKEN = "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" 
    
    # Initialize the engine
    ner = HuggingFaceNER(MY_TOKEN)
    
    # Test Data
    sample_text = """
    Alphabet Inc. announced that Google Cloud generated $15.2 billion in revenue. 
    Sundar Pichai said the company is expanding in California and New York.
    """
    
    print("\n--- 🤖 HUGGING FACE ANALYSIS ---")
    analysis = ner.analyze(sample_text)
    
    # Print Results
    for category, items in analysis.items():
        print(f"\n[{category}]:")
        for item in items:
            print(f"  - {item}")