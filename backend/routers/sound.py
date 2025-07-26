import io
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydub import AudioSegment

from backend.database import get_db
from backend.models.sound import SoundFile
from backend.models.tag import Tag
from backend.schemas.sound import Sound
from backend.services.gpt_service import get_tags_from_gpt

router = APIRouter(tags=["sounds"])

# ===========================
# 사운드 업로드
# ===========================
@router.post("/", response_model=Sound)
async def upload_sound(
    name: str = Form(...),
    tags: str = Form(...),  # 쉼표로 구분된 태그 이름들
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. 파일 읽기
    raw_data = await file.read()
    input_format = file.filename.split(".")[-1].lower()

    # 2. mp3 변환
    try:
        sound = AudioSegment.from_file(io.BytesIO(raw_data), format=input_format)
        mp3_io = io.BytesIO()
        sound.export(mp3_io, format="mp3")
        mp3_bytes = mp3_io.getvalue()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"파일 변환 실패: {str(e)}")

    # 3. 중복 파일 검사
    exists = db.query(SoundFile).filter(SoundFile.data == mp3_bytes).first()
    if exists:
        return exists  # 이미 존재하면 그대로 반환

    # 4. 새 사운드 객체 생성
    new_sound = SoundFile(name=name, data=mp3_bytes, mime_type="audio/mpeg")

    # 5. 태그 연결 (없는 태그면 자동 생성)
    tag_names = [t.strip() for t in tags.split(",") if t.strip()]
    for tag_name in tag_names:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            # 새로운 태그를 먼저 생성
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()  # ID 확보 (commit보다 가볍게 세션 반영)
        new_sound.tags.append(tag)

    db.add(new_sound)
    db.commit()
    db.refresh(new_sound)

    return new_sound


# ===========================
# 사운드 스트리밍
# ===========================
@router.get("/{sound_id}")
def get_sound(sound_id: int, db: Session = Depends(get_db)):
    sound = db.query(SoundFile).filter(SoundFile.id == sound_id).first()
    if not sound:
        raise HTTPException(status_code=404, detail="Sound not found")
    return StreamingResponse(io.BytesIO(sound.data), media_type=sound.mime_type)


# ===========================
# 태그로 사운드 검색
# ===========================
@router.get("/search", response_model=List[Sound])
def search_sounds(tag_id: int, db: Session = Depends(get_db)):
    sounds = db.query(SoundFile).filter(SoundFile.tags.any(id=tag_id)).all()
    return sounds


# ===========================
# GPT를 통한 AI 검색
# ===========================
@router.post("/ai_search")
async def ai_search(
    prompt: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    ai_tags = await get_tags_from_gpt(prompt, db)

    sounds = (
        db.query(SoundFile)
        .join(SoundFile.tags)
        .filter(Tag.name.in_(ai_tags))
        .all()
    )

    results = [
        {
            "id": s.id,
            "name": s.name,
            "mime_type": s.mime_type,
            "tags": [t.name for t in s.tags]
        }
        for s in sounds
    ]

    return {"tags": ai_tags, "results": results}
