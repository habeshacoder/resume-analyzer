from fastapi import UploadFile, File, HTTPException
import os
import requests
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_file(file: UploadFile):
    """
    Save the uploaded file to the specified directory
    """
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return file_location

async def send_to_n8n(file_location: str, filename: str, uploaded_by: str):
    """
    Send the file details to the n8n webhook
    """
    payload = {
        "file_path": file_location,
        "filename": filename,
        "uploaded_by": uploaded_by
    }
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        response.raise_for_status()  # Raise an error if the request failed
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to notify n8n: {e}")

async def handle_upload(file: UploadFile, username: str):
    """
    Handle the file upload and notify n8n.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_location = await save_file(file)
    await send_to_n8n(file_location, file.filename, username)
    return JSONResponse(content={"message": f"File '{file.filename}' saved and sent to n8n."})
