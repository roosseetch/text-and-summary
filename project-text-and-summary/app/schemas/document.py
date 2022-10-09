from typing import Sequence

from pydantic import BaseModel, validator, Field

from app.utils.decorators import as_form
from app.utils.string_utils import strip_special_characters

@as_form
class DocumentCreate(BaseModel):
    text: str = Field(..., min_length=1)

    @validator('text')
    def validate_text(cls, text):
        text = strip_special_characters(text)
        if not text:
            raise ValueError('Text should contain not special characters')
        return text


class DocumentUpdate(DocumentCreate):
    ...

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
