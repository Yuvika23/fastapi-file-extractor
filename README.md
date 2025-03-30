📌 Complete Setup Guide for Backend (FastAPI) – File Upload & Text Extraction
This guide will help you set up, run, and deploy a FastAPI backend that allows users to upload PDF, Word, and Excel files and extract text from them.

🔹 1. Prerequisites
Ensure you have the following installed:
✅ Python 3.10+ (Check with python --version)
✅ pip (Check with pip --version)
✅ Visual Studio Code (VS Code) (Recommended)
✅ Git (Optional, for GitHub)

🔹 2. Project Setup
📂 Create a New Project Folder
Open CMD or Terminal and run:

mkdir fastapi-file-extraction
cd fastapi-file-extraction

🔧 Create a Virtual Environment

python -m venv venv

Activate the virtual environment:

Windows (CMD): venv\Scripts\activate

Windows (PowerShell): .\venv\Scripts\Activate

Mac/Linux: source venv/bin/activate

🔹 3. Install Dependencies

pip install fastapi uvicorn python-multipart pymupdf python-docx pandas openpyxl

🔹 4. Create main.py (FastAPI Backend)
Inside your project folder, create a main.py file and paste this code:


from fastapi import FastAPI, File, UploadFile
import fitz  # PyMuPDF for PDFs
from docx import Document  # For Word files
import pandas as pd  # For Excel files
import os

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text
    extracted_text = extract_text(file_path)

    return {"filename": file.filename, "extracted_text": extracted_text}

def extract_text(file_path):
    file_ext = file_path.split(".")[-1].lower()

    if file_ext == "pdf":
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text("text") for page in doc])
    elif file_ext in ["doc", "docx"]:
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    elif file_ext in ["xls", "xlsx"]:
        df = pd.read_excel(file_path)
        text = df.to_string()
    else:
        return "Unsupported file format"

    return text
🔹 5. Run the FastAPI Server
Start the FastAPI backend using:

uvicorn main:app --reload
You should see:

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

🔹 6. Test the API (Swagger UI)
Open your browser and go to http://127.0.0.1:8000/docs

Click on /upload/ → Try it out → Upload a file → Execute

Check the extracted text.

✅ If it works, your backend is ready! 🎉
