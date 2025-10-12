from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.uploads import router as uploads_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

# ✅ CORS 설정 (라우터 등록 전에 적용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터 등록
app.include_router(uploads_router)


@app.get("/")
async def root():
    return {"message": "Backend is running!"}

# 개발 환경에서만 직접 실행 가능하도록
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
