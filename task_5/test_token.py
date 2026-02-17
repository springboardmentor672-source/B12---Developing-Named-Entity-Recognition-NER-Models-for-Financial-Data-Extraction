import requests

# --- PASTE YOUR NEW TOKEN HERE ---
# Make sure there are no spaces inside the quotes!
MY_TOKEN = "YOUR_TOKEN_HERE" 

API_URL = "https://router.huggingface.co/hf-inference/models/ProsusAI/finbert"
headers = {"Authorization": f"Bearer {MY_TOKEN}"}

print(f"Testing Token: {MY_TOKEN[:10]}...") 

try:
    response = requests.post(API_URL, headers=headers, json={"inputs": "I love profit."})
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Your token is working.")
        print("Response:", response.json())
    else:
        print(f"\n❌ FAILED. Error {response.status_code}")
        print("Reason:", response.text)

except Exception as e:
    print("\n❌ CONNECTION ERROR:", e)