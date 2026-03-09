import os
from dotenv import load_dotenv
from groq import Groq

# Loading environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initializing Groq client
client = Groq(api_key=api_key)

# Reading markdown input
with open("input.md", "r", encoding="utf-8") as file:
    financial_text = file.read()

financial_text = financial_text[:4000]

# AI prompt
prompt = f"""
You are a financial analyst.

Analyze the financial report below and produce:

1. Key Trends
2. Potential Risks
3. Business Insights
4. Recommendations

Financial Report:
{financial_text}
"""

# Calling Groq model
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=500
)

# Output
print("\n-----Financial Insights-----\n")
print(response.choices[0].message.content)