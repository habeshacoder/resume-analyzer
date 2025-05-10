import os
import requests
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def handle_upload(file):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Send to n8n
    payload = {
        "file_path": file_location,
        "filename": file.filename
    }
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        response.raise_for_status()  # Check if the request was successful
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to notify n8n: {e}")

    return JSONResponse(content={"message": f"File '{file.filename}' saved and sent to n8n."})
