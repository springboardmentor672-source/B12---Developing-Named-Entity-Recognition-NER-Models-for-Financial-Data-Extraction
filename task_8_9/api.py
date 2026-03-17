import os
import json
import pymupdf4llm
import textwrap
import langextract as lx
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

try:
    from sentiment_module import FinancialSentiment
    from llm_analysis import LLMAnalyst
except ImportError:
    print("⚠️ Warning: Could not import custom modules. Make sure sentiment_module.py and llm_analysis.py exist in this folder.")

# --- API KEYS ---
# Make sure to use your fresh Google API key!
HF_TOKEN = "HF_TOKEN"
GEMINI_KEY = "Google API key"

# Initialize the FastAPI app
app = FastAPI(
    title="Financial AI Pipeline API",
    description="API for PDF Conversion, Sentiment, NER, and LLM Insights.",
    version="2.0"
)

# --- CORS SETUP ---
# This allows your React frontend (port 5173) to talk to this API (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to ["http://localhost:5173"] for tighter security later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REQUEST MODELS ---
class TextRequest(BaseModel):
    text: str
    filename: str = "financial_document" # Default name if none is provided

# --- ROUTES ---

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.post("/convert/")
async def convert_pdf_to_md(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    temp_file_path = f"temp_{file.filename}"
    base_name = os.path.splitext(file.filename)[0]
    final_output_path = os.path.join(output_folder, f"{base_name}.md")
    
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
            
        print(f"📄 Converting: {file.filename}...")
        md_text = pymupdf4llm.to_markdown(temp_file_path)
        
        with open(final_output_path, "w", encoding="utf-8") as f:
            f.write(md_text)
            
        os.remove(temp_file_path)
        
        return {
            "status": "success",
            "message": f"Saved to {final_output_path}",
            "markdown_content": md_text
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/sentiment/")
async def analyze_sentiment(req: TextRequest):
    print("📊 Running Sentiment Analysis...")
    analyzer = FinancialSentiment(HF_TOKEN)
    results = analyzer.analyze(req.text[:1500]) 
    
    # Save to JSON
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    clean_filename = req.filename.replace(".pdf", "").replace(".md", "")
    final_output_path = os.path.join(output_folder, f"{clean_filename}_sentiment.json")
    
    with open(final_output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    return {
        "status": "success",
        "saved_location": final_output_path,
        "total_sentences_analyzed": len(results),
        "results": results
    }


@app.post("/analyze/memo/")
async def analyze_memo(req: TextRequest):
    print("🧠 Generating Investment Memo...")
    analyst = LLMAnalyst(GEMINI_KEY)
    insight = analyst.generate_insight(req.text[:30000])
    
    # Save to Markdown
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    clean_filename = req.filename.replace(".pdf", "").replace(".md", "")
    final_output_path = os.path.join(output_folder, f"{clean_filename}_memo.md")
    
    with open(final_output_path, "w", encoding="utf-8") as f:
        f.write(insight)
        
    return {
        "status": "success",
        "saved_location": final_output_path,
        "memo": insight
    }


@app.post("/analyze/ner/")
async def analyze_ner(req: TextRequest):
    os.environ["LANGEXTRACT_API_KEY"] = GEMINI_KEY
    print("📌 Extracting Entities...")
    
    prompt = textwrap.dedent("""\
        Extract all finance-related entities from the text.
        Focus on classes: 'company', 'metric', 'executive', 'sentiment'.
    """)
    
    examples = [
        lx.data.ExampleData(
            text="AlphaTech's CEO, Jane Doe, announced a quarterly revenue of $2.5 billion, signaling a strongly bullish outlook.",
            extractions=[
                lx.data.Extraction(extraction_class="company", extraction_text="AlphaTech"),
                lx.data.Extraction(extraction_class="executive", extraction_text="Jane Doe"),
                lx.data.Extraction(extraction_class="metric", extraction_text="quarterly revenue of $2.5 billion"),
                lx.data.Extraction(extraction_class="sentiment", extraction_text="strongly bullish outlook"),
            ]
        )
    ]
    
    try:
        result = lx.extract(
            text_or_documents=req.text[:3000],
            prompt_description=prompt,
            examples=examples,
            model_id="gemini-2.5-flash"
        )
        
        extractions = [
            {"class": ext.extraction_class, "text": ext.extraction_text, "attributes": ext.attributes}
            for ext in result.extractions
        ]
        
        # Save to JSON
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        clean_filename = req.filename.replace(".pdf", "").replace(".md", "")
        final_output_path = os.path.join(output_folder, f"{clean_filename}_ner.json")
        
        with open(final_output_path, "w", encoding="utf-8") as f:
            json.dump(extractions, f, indent=4)
        
        return {
            "status": "success",
            "saved_location": final_output_path,
            "entities": extractions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting FastAPI Server...")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)