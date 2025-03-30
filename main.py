from fastapi import FastAPI, File, UploadFile
import fitz  # PyMuPDF
from docx import Document
import pandas as pd
import os

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
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
