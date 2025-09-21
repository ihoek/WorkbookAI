from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.uploads import router as uploads_router

app = FastAPI()

# ✅ 라우터 등록
app.include_router(uploads_router)

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # 프론트엔드 origin 명시
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend is running!"}
