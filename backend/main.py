from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine

# ✅ 새로 만든 라우터들 임포트
from backend.routers.tag import router as tag_router
from backend.routers.sound import router as sound_router
from backend.routers.sound_tag import router as sound_tag_router  # 선택적

# ✅ 모델들을 임포트해서 메타데이터에 등록
from backend.models import sound, tag, sound_tag

# ✅ DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

# ✅ FastAPI 앱 생성
app = FastAPI(title="MoodSound API")

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요한 도메인만 넣어도 됨
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터 등록
app.include_router(tag_router, prefix="/api/tags", tags=["tags"])
app.include_router(sound_router, prefix="/api/sounds", tags=["sounds"])
app.include_router(sound_tag_router, prefix="/api/sound-tags", tags=["sound-tags"])  # 필요 시

# ✅ 개발 시 uvicorn 직접 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
