from pydantic import BaseModel
from typing import List
from backend.schemas.tag import Tag

# 사운드 생성 요청 (프론트에서 tags를 문자열로 보내므로 실제 사용은 안 할 수도 있음)
class SoundCreate(BaseModel):
    name: str
    tag_ids: List[int]

# 사운드 응답
class Sound(BaseModel):
    id: int
    name: str
    mime_type: str
    tags: List[Tag] = []

    class Config:
        orm_mode = True

# 순환 참조 방지
Sound.update_forward_refs()


