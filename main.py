from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, Base, get_db
from typing import List
from datetime import datetime, timedelta
from fastapi import status


app = FastAPI(title="Ausbildungstool Backend", description="Ein FastAPI-Projekt mit SQLite + SQLAlchemy")


Base.metadata.create_all(bind=engine)

# CORS (erlaubt lokalen Frontend-Devserver)
app.add_middleware(
    CORSMiddleware,
    # include common vite ports (5173, 5174) used by the frontend dev server
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
        "http://localhost:3000", "http://127.0.0.1:3000",
    ],
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


@app.post("/calendar", response_model=schemas.CalendarEvent, status_code=status.HTTP_201_CREATED)
def create_calendar_event(event: schemas.CalendarEventBase, db: Session = Depends(get_db)):
    """Erstellt ein neues Kalenderereignis. Erwartet das CalendarEventBase Schema (user_id, title, description, start, end, optional created)."""
    created_ts = event.created or datetime.utcnow()
    db_event = models.CalendarEvent(
        user_id=event.user_id,
        title=event.title,
        description=event.description,
        start=event.start,
        end=event.end,
        created=created_ts,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    # simple log to help debugging from dev server logs
    print(f"Created calendar event: id={db_event.id} user_id={db_event.user_id} title={db_event.title}")
    return db_event


@app.delete("/calendar/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calendar_event(event_id: int, user_id: int, db: Session = Depends(get_db)):
    """Löscht ein Kalenderereignis nach ID, prüft dabei den user_id-Parameter auf Besitzrecht."""
    db_event = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this event")
    db.delete(db_event)
    db.commit()
    return


@app.put("/calendar/{event_id}", response_model=schemas.CalendarEvent)
def update_calendar_event(event_id: int, event: schemas.CalendarEventBase, db: Session = Depends(get_db)):
    """Aktualisiert ein vorhandenes Kalenderereignis. Prüft Besitz über event.user_id."""
    db_event = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    # Ownership check: caller must provide the same user_id
    if db_event.user_id != event.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to modify this event")

    # Update only provided fields (CalendarEventBase has optional fields)
    if event.title is not None:
        db_event.title = event.title
    if event.description is not None:
        db_event.description = event.description
    if event.start is not None:
        db_event.start = event.start
    if event.end is not None:
        db_event.end = event.end

    db.commit()
    db.refresh(db_event)
    return db_event
