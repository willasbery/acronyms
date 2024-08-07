from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from ..db.core import DBAcronyms, NotFoundError


class Acronym(BaseModel):
    id: int
    acronym: str
    expansion: str
    description: Optional[str]
    keywords: Optional[list[str]]
    report_count: int = 0
    
    
class AcronymCreate(BaseModel):
    acronym: str
    expansion: str
    description: Optional[str]
    keywords: Optional[list[str]]
    report_count: int = 0
    

class AcronymUpdate(BaseModel):
    acronym: Optional[str]
    expansion: Optional[str]
    description: Optional[str]
    keywords: Optional[list[str]]
    report_count: Optional[int]
    
    
def _read_acronym(id: int, session: Session) -> DBAcronyms:
    db_acronym = session.query(DBAcronyms).filter(DBAcronyms.id == id).first()
    
    if not db_acronym: 
        raise NotFoundError(f"Acronym with id {id} not found")
    
    return db_acronym


def _read_acronyms(limit: int, session: Session) -> list[DBAcronyms]:
    if limit == 0:
        db_acronyms = session.query(DBAcronyms).all()
    else:
        db_acronyms = session.query(DBAcronyms).limit(limit).all()
        
    if not db_acronyms:
        raise NotFoundError("No acronyms found")
    
    return db_acronyms
	

def _create_acronym(acronym: AcronymCreate, session: Session) -> DBAcronyms:
    db_acronym = DBAcronyms(**acronym.model_dump(exclude_none=True))
    session.add(db_acronym)
    session.commit()
    session.refresh(db_acronym)
    
    return db_acronym


def _update_acronym(id: int, acronym: AcronymUpdate, session: Session) -> DBAcronyms:
	db_acronym = _read_acronym(id, session)
	
	for field, value in acronym.model_dump(exclude_none=True).items():
		setattr(db_acronym, field, value)
	
	session.commit()
	session.refresh(db_acronym)
	
	return db_acronym


def _delete_acronym(id: int, session: Session) -> DBAcronyms:
	db_acronym = _read_acronym(id, session)
	session.delete(db_acronym)
	session.commit()
	
	return db_acronym