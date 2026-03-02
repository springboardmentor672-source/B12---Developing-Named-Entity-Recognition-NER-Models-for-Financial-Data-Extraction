from docling.document_converter import DocumentConverter, PdfPipelineOptions
from docling.datamodel.pipeline_options import AcceleratorDevice, AcceleratorOptions
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(BASE_DIR, "input_docs", "sample.pdf")
output_dir = os.path.join(BASE_DIR, "output_text")
os.makedirs(output_dir, exist_ok=True)

# --- NEW: Pipeline Options to save memory ---
pipeline_options = PdfPipelineOptions()
# Disable OCR if you don't strictly need to read text inside images
pipeline_options.do_ocr = False 
# Reduce the number of threads to prevent memory spikes
pipeline_options.accelerator_options = AcceleratorOptions(
    num_threads=2, 
    device=AcceleratorDevice.CPU
)

# Initialize converter with these options
converter = DocumentConverter(pipeline_options=pipeline_options)

print("Starting Optimized Docling extraction (Memory Safe Mode)...")

try:
    doc = converter.convert(input_file)
    
    with open(os.path.join(output_dir, "docling.txt"), "w", encoding="utf-8") as f:
        f.write(doc.document.export_to_text())
    
    print("SUCCESS: Docling extraction completed!")
except Exception as e:
    print(f"STILL FAILING: {e}")