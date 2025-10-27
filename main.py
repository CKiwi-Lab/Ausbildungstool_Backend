from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, Base, get_db
from typing import List
from datetime import datetime, timedelta


app = FastAPI(title="Ausbildungstool Backend", description="Ein FastAPI-Projekt mit SQLite + SQLAlchemy")


Base.metadata.create_all(bind=engine)

# CORS (erlaubt lokalen Frontend-Devserver)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def seed_db(db: Session):
    # Prüfen, ob bereits Daten existieren
    if db.query(models.Document).first() or db.query(models.CalendarEvent).first():
        return

    # Beispiel-Dokumente
    docs = [
        models.Document(user_id=1, title="Dokument A", content="Inhalt A", doc_type="pdf"),
        models.Document(user_id=1, title="Dokument B", content="Inhalt B", doc_type="docx"),
        models.Document(user_id=2, title="Dokument C", content="Inhalt C", doc_type="pdf"),
    ]
    for d in docs:
        db.add(d)

    # Beispiel-Kalenderereignisse
    now = datetime.utcnow()
    events = [
        models.CalendarEvent(user_id=1, title="Meeting", description="Team Meeting", start=now, end=now + timedelta(hours=1)),
        models.CalendarEvent(user_id=1, title="Prüfung", description="Abschlussprüfung", start=now + timedelta(days=1), end=now + timedelta(days=1, hours=2)),
        models.CalendarEvent(user_id=2, title="Urlaub", description="Urlaubstage", start=now + timedelta(days=3), end=now + timedelta(days=10)),
    ]
    for e in events:
        db.add(e)

    db.commit()


@app.on_event("startup")
def on_startup():
    # Seed DB wenn leer
    db = next(get_db())
    seed_db(db)


@app.get("/", response_model=dict)
def read_root():
    return {"message": "Hello World! Dein Backend funktioniert!"}


@app.get("/documents", response_model=List[schemas.Document])
def get_documents(user_id: int, db: Session = Depends(get_db)):
    """Gibt alle Dokumente für einen Benutzer zurück. Beispiel-Query: SELECT * FROM documents WHERE user_id = x"""
    docs = db.query(models.Document).filter(models.Document.user_id == user_id).all()
    return docs


@app.get("/calendar", response_model=List[schemas.CalendarEvent])
def get_calendar(user_id: int, db: Session = Depends(get_db)):
    """Gibt alle Kalenderereignisse für einen Benutzer zurück."""
    events = db.query(models.CalendarEvent).filter(models.CalendarEvent.user_id == user_id).all()
    return events


@app.post("/calendar", response_model=schemas.CalendarEvent)
def create_calendar_event(event: schemas.CalendarEventBase, db: Session = Depends(get_db)):
    """Erstellt ein neues Kalenderereignis. Erwartet das CalendarEventBase Schema (user_id, title, description, start, end)."""
    db_event = models.CalendarEvent(
        user_id=event.user_id,
        title=event.title,
        description=event.description,
        start=event.start,
        end=event.end,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
