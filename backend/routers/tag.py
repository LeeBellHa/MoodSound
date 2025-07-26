from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.tag import Tag as TagModel  # ✅ SQLAlchemy 모델
from backend.schemas.tag import Tag, TagCreate  # ✅ Pydantic 스키마

router = APIRouter(tags=["tags"])

# -----------------------------
# 태그 생성
# -----------------------------
@router.post("/", response_model=Tag)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    # 중복 검사
    exists = db.query(TagModel).filter(TagModel.name == tag.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="이미 존재하는 태그입니다.")
    new_tag = TagModel(
        name=tag.name,
        category=tag.category,
        subcategory=tag.subcategory
    )
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

# -----------------------------
# 태그 목록
# -----------------------------
@router.get("/", response_model=List[Tag])  # 리스트로 반환
def list_tags(db: Session = Depends(get_db)):
    tags = db.query(TagModel).all()  # ✅ 여기서 TagModel 사용
    return tags
