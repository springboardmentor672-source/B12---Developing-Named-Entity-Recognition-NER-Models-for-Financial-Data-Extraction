from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os

from document_converter import convert_document

app = FastAPI(title="Document Converter API")


@app.post("/convert-pdf")
async def convert_pdf_to_markdown(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:

            content = await file.read()

            tmp_file.write(content)

            tmp_file_path = tmp_file.name

        markdown_text = convert_document(
            tmp_file_path,
            output_dir="./converted_docs"
        )

        return JSONResponse(
            content={
                "filename": file.filename,
                "status": "success"
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Conversion failed: {str(e)}"
        )

    finally:

        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)