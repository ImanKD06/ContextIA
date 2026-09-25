from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.database import Base


class Chunk(Base):

    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)

    text = Column(Text, nullable=False)

    embedding = Column(Vector(768))

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )