from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

# 업로드 파일 저장 경로
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "filepath": file_path}

@router.get("/files/list")
async def get_file_list():
    file_list = os.listdir(UPLOAD_DIR)
    return {"file_list": file_list}