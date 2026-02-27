from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader
import os

# Load API Key from .env
load_dotenv()

# Initialize LLM Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to analyze document using LLM
def analyze_document(text):
    prompt = f"""
    You are an intelligent AI document understanding assistant.

    Analyze the given document and provide:

    1. Document Type
    2. Important Key Points
    3. Required Actions
    4. Deadlines (if any)

    Document Text:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# Main Execution
if __name__ == "__main__":
    pdf_path = "sample1.pdf"

    if not os.path.exists(pdf_path):
        print("❌ sample.pdf not found in project folder")
        exit()

    print("\n📄 Reading PDF file...")
    text = extract_text_from_pdf(pdf_path)

    print("\n🤖 Sending document to AI for analysis...\n")
    result = analyze_document(text)

    print("\n=========== AI DOCUMENT ANALYSIS RESULT ===========\n")
    print(result)