from pathlib import Path
from typing import Optional, Any

from fastapi import FastAPI, APIRouter, HTTPException, Form, Depends
from sqlalchemy.orm import Session

from .schemas.document import (
    DocumentsListResponse, DocumentResponse, DocumentFullResponse,  DocumentCreate,
    DocumentSummaryResponse)
from . import deps, crud


# Project Directories
ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(title="Document API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/summaries/{document_id}", status_code=200, response_model=DocumentSummaryResponse)
def retrieve_document_summary(
    *,
    document_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve a single document summary by ID
    """
    result = crud.document.get(db=db, id=document_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Document summary with ID {document_id} not found"
        )

    return result


@api_router.get("/{document_id}", status_code=200, response_model=DocumentFullResponse)
def retrieve_document(
    *,
    document_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve a single document by ID
    """
    result = crud.document.get(db=db, id=document_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Document with ID {document_id} not found"
        )

    return result


@api_router.get("/", status_code=200, response_model=DocumentsListResponse)
def list_documents(
    *,
    skip: Optional[int] = 0,
    limit: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    List documents
    """
    documents = crud.document.get_multi(db=db, skip=skip, limit=limit)
    return {"results": documents}


@api_router.post("/", status_code=201, response_model=DocumentResponse)
def create_document(
    *,
    document_in: DocumentCreate = Depends(DocumentCreate.as_form),
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new document in the database.
    """
    document = crud.document.create(db=db, obj_in=document_in)

    return document


@api_router.put("/{document_id}", status_code=200, response_model=DocumentResponse)
def update_document(
    *,
    document_id: int,
    document_in: DocumentCreate = Depends(DocumentCreate.as_form),
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Update a document in the database.
    """
    db_obj = crud.document.get(db=db, id=document_id)
    if not db_obj:
        raise HTTPException(
            status_code=404, detail=f"Document with ID {document_id} can't be updated, not found"
        )
    document = crud.document.update(db=db, db_obj=db_obj, obj_in=document_in)

    return document


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
