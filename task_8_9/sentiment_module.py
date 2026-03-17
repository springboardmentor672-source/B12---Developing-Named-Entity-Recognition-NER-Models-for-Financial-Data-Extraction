import requests
import re
import time

class FinancialSentiment:
    def __init__(self, api_token):
        self.api_url = "https://router.huggingface.co/hf-inference/models/ProsusAI/finbert"
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def split_sentences(self, text):
        text = text.replace('\n', ' ').replace('  ', ' ')
        pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if len(s) > 15]

    def query_api(self, text):
        retries = 0
        while retries < 3:
            try:
                response = requests.post(self.api_url, headers=self.headers, json={"inputs": text})
                if response.status_code == 200:
                    return response.json()
                
                err = response.json()
                if "estimated_time" in err:
                    time.sleep(err.get('estimated_time', 5) + 1)
                    retries += 1
                    continue
                return []
            except Exception:
                return []
        return []

    def analyze(self, text):
        sentences = self.split_sentences(text)
        results = []
        for sentence in sentences:
            data = self.query_api(sentence)
            if data and isinstance(data, list) and len(data) > 0:
                first = data[0]
                if isinstance(first, list):
                    top = max(first, key=lambda x: x['score'])
                    results.append({"sentence": sentence, "label": top['label'], "score": top['score']})
                elif isinstance(first, dict) and 'label' in first:
                    top = max(data, key=lambda x: x['score'])
                    results.append({"sentence": sentence, "label": top['label'], "score": top['score']})
            time.sleep(0.3)
        return results