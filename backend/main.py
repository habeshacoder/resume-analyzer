from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from auth import authenticate_user, create_access_token, verify_token
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer Backend is running!"}

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": username})
    return {"access_token": token}

@app.get("/secure-test")
def secure_test(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        return {"message": "Secure endpoint accessed!", "user": payload["sub"]}
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = verify_token(token)
        username = payload["sub"]
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Send to n8n
    payload = {
        "file_path": file_location,
        "filename": file.filename,
        "uploaded_by": username
    }
    try:
        requests.post(N8N_WEBHOOK_URL, json=payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to notify n8n: {e}")

    return JSONResponse(content={"message": f"File '{file.filename}' saved and sent to n8n."})
