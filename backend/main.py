from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from auth import authenticate_user, create_access_token, verify_token
from fastapi.responses import JSONResponse
from upload import handle_upload  # Import the handle_upload function

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

    return await handle_upload(file, username)  # Call the function from upload.py
