from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from database import Base
from datetime import datetime


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String(255))
    content = Column(Text)
    doc_type = Column(String(50))


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String(255))
    description = Column(Text)
    start = Column(DateTime)
    end = Column(DateTime)
    created = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String(255))
    description = Column(Text)
    deadline = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    # optional FK to calendar_events table (store event id)
    calendar_event_id = Column(Integer, ForeignKey('calendar_events.id'), nullable=True)
