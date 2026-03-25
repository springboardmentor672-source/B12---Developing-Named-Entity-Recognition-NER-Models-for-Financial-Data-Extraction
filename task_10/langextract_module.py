import os
import langextract as lx
from dotenv import load_dotenv
from langextract.providers.openai import OpenAILanguageModel

load_dotenv()

groq_model = OpenAILanguageModel(
    model_id="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

PROMPT = """
Extract:
- company
- money
- percentage
- date
- product
- metric
"""

EXAMPLES = [
    lx.data.ExampleData(
        text="Apple earned $100 billion in 2023.",
        extractions=[
            lx.data.Extraction("company", "Apple"),
            lx.data.Extraction("money", "$100 billion"),
            lx.data.Extraction("date", "2023"),
        ],
    )
]

def extract_finance_entities(text: str):
    result = lx.extract(
        text_or_documents=text[:20000],
        prompt_description=PROMPT,
        examples=EXAMPLES,
        model=groq_model
    )

    output = []
    for e in result.extractions:
        output.append({
            "type": e.extraction_class,
            "text": e.extraction_text
        })

    return output