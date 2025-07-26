from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.sound_tag import sound_tag_association

class SoundFile(Base):
    __tablename__ = "sound_files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    # LONGBLOB으로 지정
    data = Column(LargeBinary(length=(2**32)-1), nullable=False, unique=True)
    mime_type = Column(String(50), default="audio/mpeg")

    # Many-to-Many 관계
    tags = relationship("Tag", secondary=sound_tag_association, backref="sounds")
