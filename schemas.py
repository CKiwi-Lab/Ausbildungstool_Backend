from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentBase(BaseModel):
    user_id: int
    title: Optional[str] = None
    content: Optional[str] = None
    doc_type: Optional[str] = None


class Document(DocumentBase):
    id: int

    class Config:
        orm_mode = True


class CalendarEventBase(BaseModel):
    user_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class CalendarEvent(CalendarEventBase):
    id: int

    class Config:
        orm_mode = True
