from pydantic import BaseModel
from typing import Optional

# 태그 생성용
class TagCreate(BaseModel):
    name: str
    category: Optional[str] = None
    subcategory: Optional[str] = None

# 태그 조회용 (응답)
class Tag(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    subcategory: Optional[str] = None

    class Config:
        orm_mode = True
