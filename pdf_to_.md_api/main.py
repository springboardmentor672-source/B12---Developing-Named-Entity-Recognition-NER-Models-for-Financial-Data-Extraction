from fastapi import FastAPI, UploadFile, File
import os
import shutil

os.environ["HF_HOME"] = "./hf_cache"
os.environ["HUGGINGFACE_HUB_CACHE"] = "./hf_cache"

from doc_converter import convert_pdf_to_markdown

app = FastAPI()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


@app.post("/convert-pdf")
async def convert_pdf(file: UploadFile = File(...)):
    try:
        temp_path = os.path.join(TEMP_DIR, file.filename)

        # Saving file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Calling external function
        markdown = convert_pdf_to_markdown(temp_path)

        os.remove(temp_path)

        return {
            "filename": file.filename,
            "markdown": markdown[:2000]
        }

    except Exception as e:
        return {"error": str(e)}