import os
import json
from openai import OpenAI
from sqlalchemy.orm import Session
from backend.models.tag import Tag  # ✅ 태그 테이블에서 직접 조회

# ✅ .env에서 API 키 불러오기
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def collect_all_tags(db: Session):
    """
    tags 테이블에서 모든 태그를 중복 없이 수집
    """
    tags = db.query(Tag).all()
    all_tags = [t.name for t in tags if t.name]
    return all_tags

async def get_tags_from_gpt(prompt: str, db: Session):
    """
    GPT에게 상황(prompt)을 주고,
    tags 테이블에서 가져온 태그 목록 중 어울리는 태그 1~3개를 JSON 배열로 추천받기
    """
    all_tags = collect_all_tags(db)
    if not all_tags:
        return []

    system_msg = (
        f"다음은 사운드 태그 목록입니다: {', '.join(all_tags)}.\n"
        "사용자가 상황을 설명하면, 위 목록에서 어울리는 태그를 1~3개 JSON 배열로 응답하세요."
    )

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ]
    )

    raw_content = chat_completion.choices[0].message.content.strip()
    try:
        tags = json.loads(raw_content)
        # GPT가 단일 문자열을 JSON 문자열로 줄 수 있으니 처리
        if isinstance(tags, str):
            tags = [tags]
    except json.JSONDecodeError:
        # JSON 파싱 실패 시 쉼표 기준 분리
        tags = [t.strip() for t in raw_content.split(",") if t.strip()]

    # DB에 실제 존재하는 태그만 필터링 (안전)
    valid_tags = []
    for t in tags:
        if t in all_tags:
            valid_tags.append(t)

    return valid_tags
