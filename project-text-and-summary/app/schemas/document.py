from typing import Sequence

from pydantic import BaseModel

from ..utils.decorators import as_form

@as_form
class DocumentCreate(BaseModel):
    text: str


@as_form
class DocumentUpdate(BaseModel):
    text: str


# Properties shared by models stored in DB
class DocumentInDBBase(BaseModel):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client only id
class DocumentResponse(DocumentInDBBase):
    pass


# Properties to return to client full
class DocumentFullResponse(DocumentInDBBase):
    text: str
    summary: str | None


# Properties to return to client summary
class DocumentSummaryResponse(DocumentInDBBase):
    summary: str


# 
class DocumentsListResponse(BaseModel):
    results: Sequence[DocumentResponse]
