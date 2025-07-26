from pydantic import BaseModel

class SoundTag(BaseModel):
    sound_id: int
    tag_id: int

    class Config:
        orm_mode = True
