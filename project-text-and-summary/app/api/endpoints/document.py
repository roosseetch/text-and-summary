from typing import Any

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.tasks import document_tasks
from app.schemas.document import (
    DocumentsListResponse, DocumentResponse, DocumentFullResponse,  DocumentCreate,
    DocumentSummaryResponse)
from app.utils.query_utils import get_db_obj_or_404


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
    error_msg = f"Document summary with ID {document_id} not found."
    return get_db_obj_or_404(obj_id=document_id, db=db, error_msg=error_msg)


@api_router.get("/{document_id}", status_code=200, response_model=DocumentFullResponse)
def retrieve_document(
    *,
    document_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve a single document by ID
    """
    error_msg = f"Document with ID {document_id} not found."
    return get_db_obj_or_404(obj_id=document_id, db=db, error_msg=error_msg)


@api_router.get("/", status_code=200, response_model=DocumentsListResponse)
def list_documents(
    *,
    skip: int | None = Query(0, ge=0, lt=9223372036854775807),
    limit: int | None = Query(10, ge=1, lt=9223372036854775807),
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    List documents
    """
    documents = crud.document.get_multi(db=db, skip=skip, limit=limit)
    return {"results": documents}


@api_router.post("/", status_code=201, response_model=DocumentResponse)
async def create_document(
    *,
    document_in: DocumentCreate = Depends(DocumentCreate.as_form),
    db: Session = Depends(deps.get_db),
    background_tasks: BackgroundTasks
) -> dict:
    """
    Create a new document in the database.
    """
    document = crud.document.create(db=db, obj_in={'text': document_in.text})

    background_tasks.add_task(document_tasks.generate_summary_for_text.delay, document.id)

    return document


@api_router.put("/{document_id}", status_code=200, response_model=DocumentResponse)
async def update_document(
    *,
    document_id: int,
    document_in: DocumentCreate = Depends(DocumentCreate.as_form),
    db: Session = Depends(deps.get_db),
    background_tasks: BackgroundTasks
) -> dict:
    """
    Update a document in the database.
    """
    error_msg = f"Document with ID {document_id} can't be updated, not found."
    db_obj = get_db_obj_or_404(obj_id=document_id, db=db, error_msg=error_msg)
    document = crud.document.update(db=db, db_obj=db_obj, obj_in=document_in)

    background_tasks.add_task(document_tasks.generate_summary_for_text.delay, document.id)

    return document
