from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session

from ..db.core import NotFoundError, get_db
from ..db.acronyms import (
  Acronym,
  AcronymCreate,
  AcronymUpdate,
  _read_acronym, 
  _read_acronyms, 
  _create_acronym, 
  _update_acronym, 
  _delete_acronym)


router = APIRouter()

  
@router.get("/{acronym_id}")
async def read_acronym_by_id(acronym_id: int, db: Session = Depends(get_db)) -> Acronym:
    try:
        acronym = _read_acronym(acronym_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Acronym(**acronym.__dict__)


@router.get("/")
async def read_acronyms_list(limit: int = 0, db: Session = Depends(get_db)) -> list[Acronym]:
	try:
		acronyms = _read_acronyms(limit, db)
	except NotFoundError as e:
		raise HTTPException(status_code=404, detail=str(e))
	return [Acronym(**acronym.__dict__) for acronym in acronyms]


@router.post("/")
async def create_acronym(acronym: AcronymCreate, db: Session = Depends(get_db)) -> Acronym:
    new_acronym = _create_acronym(acronym, db)
    return Acronym(**new_acronym.__dict__)


@router.put("/{acronym_id}")
async def update_acronym(acronym_id: int, acronym: AcronymUpdate, db: Session = Depends(get_db)) -> Acronym:
	try:
		updated_acronym = _update_acronym(acronym_id, acronym, db)
	except NotFoundError as e:
		raise HTTPException(status_code=404, detail=str(e))
	return Acronym(**updated_acronym.__dict__)


@router.delete("/{acronym_id}")
async def delete_acronym(acronym_id: int, db: Session = Depends(get_db)) -> Acronym:
	try:
		deleted_acronym = _delete_acronym(acronym_id, db)
	except NotFoundError as e:
		raise HTTPException(status_code=404, detail=str(e))
	return Acronym(**deleted_acronym.__dict__)