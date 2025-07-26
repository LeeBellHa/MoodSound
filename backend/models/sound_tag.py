from sqlalchemy import Table, Column, Integer, ForeignKey
from backend.database import Base

sound_tag_association = Table(
    "sound_tags",
    Base.metadata,
    Column("sound_id", Integer, ForeignKey("sound_files.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
