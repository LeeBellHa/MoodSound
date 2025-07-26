# 임시 스크립트 (예: backend/seed_tags.py)
from backend.database import SessionLocal
from backend.models.tag import Tag

tags_to_insert = [
    "도시", "자연", "실내", "실외",
    "걸음", "타격", "문닫기",
    "긍정", "부정", "없음",
    "남성", "여성", "무성",
    "도구", "기계",
    "UI긍정", "UI부정", "UI없음"
]

db = SessionLocal()
for t in tags_to_insert:
    if not db.query(Tag).filter_by(name=t).first():
        db.add(Tag(name=t))
db.commit()
db.close()
print("✅ 태그 초기 데이터 입력 완료")
