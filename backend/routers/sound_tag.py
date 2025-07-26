from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.sound import SoundFile
from backend.models.tag import Tag

router = APIRouter(tags=["sound-tags"])

# 사운드에 태그 추가
@router.post("/add")
def add_tag_to_sound(sound_id: int, tag_id: int, db: Session = Depends(get_db)):
    sound = db.query(SoundFile).get(sound_id)
    tag = db.query(Tag).get(tag_id)
    if not sound or not tag:
        raise HTTPException(status_code=404, detail="Sound or Tag not found")
    if tag in sound.tags:
        return {"message": "이미 연결된 태그"}
    sound.tags.append(tag)
    db.commit()
    return {"message": "태그 추가 완료"}

# 사운드에서 태그 제거
@router.delete("/remove")
def remove_tag_from_sound(sound_id: int, tag_id: int, db: Session = Depends(get_db)):
    sound = db.query(SoundFile).get(sound_id)
    tag = db.query(Tag).get(tag_id)
    if not sound or not tag:
        raise HTTPException(status_code=404, detail="Sound or Tag not found")
    if tag not in sound.tags:
        return {"message": "연결되지 않은 태그"}
    sound.tags.remove(tag)
    db.commit()
    return {"message": "태그 제거 완료"}
