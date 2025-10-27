# Ausbildungstool_Backend

Dieses Repository enthält ein kleines FastAPI-Backend mit einer SQLite-Datenbank (SQLAlchemy). Es dient als einfache API für das Frontend (azubitool_frontend) und stellt Endpunkte bereit, mit denen Dokumente und Kalenderereignisse pro Benutzer abgefragt werden können.

## Übersicht

- Sprache: Python
- Framework: FastAPI
- DB: SQLite (via SQLAlchemy)
- Start: `uvicorn main:app --reload`

## Dateien

- `main.py` - FastAPI-App, Endpunkte und DB-Seeding
- `database.py` - SQLAlchemy Engine, Session und Base
- `models.py` - ORM-Modelle (`Document`, `CalendarEvent`)
- `schemas.py` - Pydantic-Schemas für Responses
- `requirements.txt` - Abhängigkeiten

## Datenmodell (vereinfacht)

Tabelle `documents` (SQL):

SELECT * FROM documents WHERE user_id = x

Spalten: id, user_id, title, content, doc_type

Tabelle `calendar_events` (SQL):

SELECT * FROM calendar_events WHERE user_id = x

Spalten: id, user_id, title, description, start, end

## API Endpunkte

Alle Endpunkte erwarten standardmäßig keine speziellen Header außer Standard-HTTP-Headern (Content-Type bei POST/PUT). Die Beispiel-Endpunkte sind GET-Requests und erhalten den Parameter `user_id` als Query-Parameter.

1) GET /documents

- Beschreibung: Liefert alle Dokumente für einen gegebenen `user_id`.
- URL: http://127.0.0.1:8000/documents?user_id=1
- Query-Parameter: `user_id` (int) — die ID des Benutzers
- Response: JSON-Array von Dokumenten (siehe Schema `Document`)
- Beispiel-DB-Query: `SELECT * FROM documents WHERE user_id = x`

2) GET /calendar

- Beschreibung: Liefert alle Kalenderereignisse für einen gegebenen `user_id`.
- URL: http://127.0.0.1:8000/calendar?user_id=1
- Query-Parameter: `user_id` (int)
- Response: JSON-Array von Kalenderereignissen (siehe Schema `CalendarEvent`)

3) GET / (Root)

- Liefert nur eine Health/Welcome-Nachricht.

## Schemas (Response)

- Document: { id, user_id, title, content, doc_type }
- CalendarEvent: { id, user_id, title, description, start, end }

## Beispiel-Workflow für das Frontend

1. Frontend ruft `GET /documents?user_id=42` auf.
2. Backend führt intern `SELECT * FROM documents WHERE user_id = 42` aus (SQLAlchemy Query) und gibt das Ergebnis als JSON zurück.
3. Frontend befüllt Tabellen oder Listen mit den zurückgegebenen Objekten.

Gleiches gilt für `GET /calendar`.

## Setup & Start (Windows / PowerShell)

1) Ins Projektverzeichnis wechseln:

```powershell
Set-Location -Path "C:\Users\christopherki\Ausbildungstool_Backend"
```

2) Virtuelle Umgebung erstellen und aktivieren:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Abhängigkeiten installieren:

```powershell
pip install -r requirements.txt
```

4) Server starten:

```powershell
uvicorn main:app --reload
```

API-Dokumentation (Swagger) ist verfügbar unter: http://127.0.0.1:8000/docs

## Hinweise / nächste Schritte

- Aktuell sind nur GET-Endpunkte implementiert. Für Erstellung/Update/Deletion (`POST/PUT/DELETE`) können weitere Endpunkte ergänzt werden.
- Authentifizierung ist derzeit nicht implementiert. Für produktive Nutzung empfiehlt sich Token-basierte Auth (z. B. OAuth2 / JWT).
- Filter, Paging und Suchfunktionen können hinzugefügt werden, um Frontend-Abfragen effizienter zu machen.
# Ausbildungstool_Backend
For the programming language python
