## **Backend Setup**

Bash

\# Navigate to the backend directory (or root if backend is in root)

\# Create and activate virtual environment

python -m venv venv

source venv/bin/activate  # On Windows use: venv\\\\Scripts\\\\activate



\# Install dependencies

pip install fastapi uvicorn python-multipart pymupdf4llm pymupdf langextract python-dotenv requests



\# Create your environment variables file

\# Add GEMINI\_API\_KEY and HF\_TOKEN to a new .env file



\# Start the server

uvicorn api:app --reload





## **Frontend Setup**

Bash

\# Open a new terminal and navigate to the frontend directory

cd frontend



\# Install dependencies

npm install axios react-markdown



\# Start the development server

npm run dev

💡 How to Use

Open the React dashboard (http://localhost:5173).



Click Choose File and upload a financial PDF.



Click Initialize Analysis.



The pipeline will parse the file, trigger the Gemini, LangExtract, and FinBERT models, and dynamically render the results.



Generated data is automatically archived locally in the backend's output/ folder.

