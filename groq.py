from groq import Groq

# 🔐 Paste your Groq API key here
client = Groq(api_key="YOUR_GROQ_API_KEY")


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an expert ATS (Applicant Tracking System).

Analyze the resume against the job description.

Provide the response clearly in sections:

1. Key Skills Found
2. Missing Skills
3. Match Percentage (0-100%)
4. Suggestions to Improve

Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = client.chat.completions.create(
      model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ==============================
# SAMPLE RESUME TEXT
# ==============================
resume = """
Lena Mathew
Email: lenamathew@gmail.com
Phone: 9876543210

Professional Summary:
Motivated Python Developer with 2 years of experience in data analysis and machine learning.
Strong knowledge of Python, SQL, and data visualization.

Technical Skills:
- Python
- SQL
- Pandas
- NumPy
- Scikit-learn
- TensorFlow
- MySQL
- Machine Learning

Projects:
1. Customer Churn Prediction - 85% accuracy using Scikit-learn
2. Sales Dashboard using Python and data visualization
"""

# ==============================
# SAMPLE JOB DESCRIPTION
# ==============================
job_desc = """
Job Title: Data Scientist

We are looking for a Data Scientist with strong experience in:

- Python
- SQL
- Machine Learning
- Deep Learning
- NLP (Natural Language Processing)
- TensorFlow or PyTorch
- Model Deployment
"""

# ==============================
# RUN ANALYSIS
# ==============================
if __name__ == "__main__":

    print("========== Resume Analyzer (Groq) ==========\n")

    result = analyze_resume(resume, job_desc)

    print("\n========== Analysis Result ==========\n")
    print(result)