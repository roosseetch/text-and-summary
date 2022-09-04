from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Document(Base):
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
