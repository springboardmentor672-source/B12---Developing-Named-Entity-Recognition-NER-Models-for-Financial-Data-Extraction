from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

# Import modules
from ner_module import extract_entities
from sentiment_module import analyze_sentiment
from langextract_module import extract_finance_entities

app = FastAPI(title="Finance AI API 🚀")

# ---------------- NER ----------------
@app.post("/ner")
async def ner_api(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8")
    return {"entities": extract_entities(text)}


# ---------------- SENTIMENT ----------------
@app.post("/sentiment")
async def sentiment_api(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8")
    return {"sentiment": analyze_sentiment(text)}


# ---------------- LANGEXTRACT ----------------
@app.post("/langextract")
async def langextract_api(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8")

    try:
        result = extract_finance_entities(text)
        return {"entities": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {"message": "API Running ✅"}