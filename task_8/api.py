import os
import pymupdf4llm
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn

# Initialize the FastAPI app
app = FastAPI(
    title="Financial Document Parser API",
    description="API to convert financial PDFs into LLM-ready Markdown and save them locally.",
    version="1.0"
)

@app.get("/")
def read_root():
    """Redirects the base URL straight to the interactive API docs."""
    return RedirectResponse(url="/docs")

@app.post("/convert/")
async def convert_pdf_to_md(file: UploadFile = File(...)):
    """Uploads a PDF, converts it, and saves the Markdown file to the output folder."""
    
    # 1. Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    # 2. Setup folders and paths
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True) # Creates 'output' folder if it doesn't exist
    
    temp_file_path = f"temp_{file.filename}"
    
    # Create the final output filename (e.g., earnings.pdf -> earnings.md)
    base_name = os.path.splitext(file.filename)[0]
    final_output_path = os.path.join(output_folder, f"{base_name}.md")
    
    try:
        # 3. Save the uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
            
        # 4. Convert PDF to Markdown
        print(f"📄 Processing: {file.filename}...")
        md_text = pymupdf4llm.to_markdown(temp_file_path)
        
        # 5. SAVE THE MARKDOWN FILE TO DISK
        with open(final_output_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        print(f"✅ Saved Markdown file to: {final_output_path}")
        
        # 6. Clean up the temporary PDF file
        os.remove(temp_file_path)
        
        # 7. Return a clean JSON response confirming the save location
        return {
            "status": "success",
            "original_file": file.filename,
            "saved_location": final_output_path,
            "message": f"Successfully saved to {final_output_path}"
        }
        
    except Exception as e:
        # Ensure cleanup happens even if it crashes
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")

# --- SERVER RUNNER ---
if __name__ == "__main__":
    print("🚀 Starting FastAPI Server...")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)