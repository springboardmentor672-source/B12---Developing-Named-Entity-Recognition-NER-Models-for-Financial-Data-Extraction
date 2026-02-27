import os
from dotenv import load_dotenv
import requests
import PyPDF2

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

def check_compliance(policy_text, scenario_text):

    prompt = f"""
You are a corporate compliance assistant.

Analyze the scenario strictly based on the company policy.

Return the result in the EXACT format below.
Do not add extra text outside this format.

FORMAT:

COMPLIANCE STATUS:
(Compliant or Non-Compliant)

VIOLATED RULES:
- Rule 1
- Rule 2

RISK LEVEL:
(Low / Medium / High)

REASON:
(Short explanation in 3-5 lines)

CORRECTIVE ACTIONS:

Immediate Actions:
- Action 1
- Action 2

Preventive Actions:
- Action 1
- Action 2

----------------------------------------

Company Policy:
{policy_text}

Scenario:
{scenario_text}
"""

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]

if __name__ == "__main__":

    policy_text = read_pdf("sample_policy.pdf")
    scenario_text = read_pdf("sample_scenario.pdf")

    output = check_compliance(policy_text, scenario_text)

    print("\n==============================")
    print("  POLICY COMPLIANCE ANALYSIS")
    print("==============================\n")

    print(output)