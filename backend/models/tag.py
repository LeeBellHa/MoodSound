from sqlalchemy import Column, Integer, String
from backend.database import Base

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=True)
    subcategory = Column(String(50), nullable=True)
    name = Column(String(50), unique=True, nullable=False)
