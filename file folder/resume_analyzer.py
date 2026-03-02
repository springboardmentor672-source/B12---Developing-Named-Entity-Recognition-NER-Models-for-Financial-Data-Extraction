import os
from typing import Optional
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def read_resume(file_path: str) -> Optional[str]:
    if not os.path.isfile(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    if not content.strip():
        return None

    return content


def analyze_resume(resume_text: str):

    prompt = f"""
You are a professional HR analyst and career consultant.

Analyze the resume below and extract:

1. Technical Skills (list format)
2. Soft Skills (list format)
3. Estimated Experience Level (Fresher / Junior / Mid-Level / Senior)
4. Suggested Job Roles (3 roles)
5. Overall Profile Strength (Weak / Moderate / Strong)
6. Short Career Improvement Suggestion

Resume:
{resume_text}

Return structured output clearly.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":

    print("AI Resume Analyzer")
    print("-" * 40)

    file_path = "sample_resume.txt"

    resume_text = read_resume(file_path)

    if not resume_text:
        print("Error: Resume file not found or empty.")
        exit()

    result = analyze_resume(resume_text)

    print("\n Resume Analysis Result:\n")
    print(result)