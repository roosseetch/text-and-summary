from typing import  Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud

def get_db_obj_or_404(
    *,
    obj_id: int,
    db: Session,
    error_msg: str | None = None
) -> Any :
    db_obj = crud.document.get(db=db, id=obj_id)
    if not db_obj:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        error_msg = error_msg or f"Object with ID {obj_id} not found."
        raise HTTPException(status_code=404, detail=error_msg)
    
    return db_obj
