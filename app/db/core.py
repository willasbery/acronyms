from typing import Optional, List
from sqlalchemy import create_engine, JSON
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

from ..config.config import settings


class NotFoundError(Exception):
  pass


class Base(DeclarativeBase):
  pass


class DBAcronyms(Base):
  __tablename__ = "acronyms"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  acronym: Mapped[str] 
  expansion: Mapped[str]
  description: Mapped[Optional[str]]
  keywords: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
  report_count: Mapped[int] = mapped_column(default=0)
  

engine = create_engine(settings.DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


async def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()