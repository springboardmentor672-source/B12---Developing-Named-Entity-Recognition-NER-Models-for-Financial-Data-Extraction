import fitz  # PyMuPDF
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI(title="PDF to Markdown API")


# =====================================
# CORE FUNCTION: PDF → Markdown
# =====================================
def convert_pdf_to_md(file_bytes):

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    md_text = ""

    for page_num, page in enumerate(doc):
        md_text += f"\n\n# Page {page_num + 1}\n\n"
        md_text += page.get_text()

    doc.close()
    return md_text


# =====================================
# API ENDPOINT
# =====================================
@app.post("/convert-pdf-to-md/")
async def convert_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return JSONResponse(
            status_code=400,
            content={"error": "Only PDF files are allowed"}
        )

    try:
        pdf_bytes = await file.read()

        md_text = convert_pdf_to_md(pdf_bytes)

        return {
            "filename": file.filename,
            "markdown": md_text[:2000]  # limit response size
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )