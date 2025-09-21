from fastapi import APIRouter, UploadFile, File
import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import PyPDF2
import docx
import uuid

router = APIRouter()

# 업로드 파일 저장 경로
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ KURE 임베딩 모델
embed_model = SentenceTransformer("nlpai-lab/KURE-v1")

# ✅ Qdrant 클라이언트 연결 (로컬: http://localhost:6333)
qdrant = QdrantClient(host="localhost", port=6333)

# ✅ 컬렉션 생성 (없으면 자동 생성)
COLLECTION_NAME = "documents"
if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),  # KURE-v1 차원=768
    )

def extract_text(file_path: str, ext: str) -> str:
    """파일 확장자에 따라 텍스트 추출"""
    text = ""
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == ".docx":
        doc = docx.Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("지원하지 않는 파일 형식")
    return text.strip()

# 파일 업로드 및 Qdrant에 저장 요청
@router.post("/upload-analyze")
async def upload_and_analyze(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    _, ext = os.path.splitext(file.filename)
    try:
        text = extract_text(file_path, ext.lower())
    except Exception as e:
        return {"error": str(e)}

    # ✅ KURE 임베딩 생성
    embedding = embed_model.encode([text])[0]

    # ✅ Qdrant에 저장 (문서 전체를 하나의 point로 저장)
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=hash(uuid.uuid4()),  # 고유 ID (간단히 파일명 해시 사용)
                vector=embedding.tolist(),
                payload={"filename": file.filename, "content": text[:200]}  # 일부 텍스트만 저장
            )
        ]
    )

    return {
        "filename": file.filename,
        "embedding_dim": len(embedding),
        "status": "saved_to_qdrant"
    }

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "filepath": file_path}

# 파일 리스트 전체 조회 요청
@router.get("/files/list")
async def get_file_list():
    file_list = os.listdir(UPLOAD_DIR)
    return {"file_list": file_list}