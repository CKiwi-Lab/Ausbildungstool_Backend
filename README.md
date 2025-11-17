# Ausbildungstool_Backend

Dieses Repository enthält das Backend für das Azubitool-Projekt. Es ist als leichtes Entwicklungs-Backend konzipiert (FastAPI + SQLite) und stellt die API-Endpunkte bereit, die das Frontend (`azubitool_frontend`) erwartet.

Kurz: Das Backend bietet Endpunkte für Kalenderereignisse und Dokumente, persistiert Daten in `azubi.db` (SQLite) und ist lokal mit `uvicorn` lauffähig.

## Übersicht

- Sprache: Python 3.11+ / 3.12+
- Framework: FastAPI
- DB: SQLite über SQLAlchemy (vereinfacht, für Entwicklung)
- Start (Entwicklung): `python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000`

## Projektstruktur

- `main.py` – FastAPI-Anwendung, Endpunkte, CORS, DB-Seeding
- `database.py` – SQLAlchemy Engine, SessionLocal, Base, get_db()
- `models.py` – SQLAlchemy ORM-Modelle (`Document`, `CalendarEvent`)
- `schemas.py` – Pydantic-Schemas (Request/Response)
- `requirements.txt` – benötigte Python-Pakete
- `azubi.db` – SQLite-Datenbank (lokal, wird erstellt/seeded)
- `Projektantrag.md` – Projektantrag / Übersicht (informativ)

## Datenmodell

Tabelle `documents`:
- id: Integer PK
- user_id: Integer
- title: String
- content: Text
- doc_type: String

Tabelle `calendar_events`:
- id: Integer PK
- user_id: Integer
- title: String
- description: Text
- start: DateTime
- end: DateTime
- created: DateTime (neu; wurde per Migration / ALTER TABLE ergänzt)

Hinweis: Die Datenbankspalte `created` wurde nachträglich ergänzt — beim Start erstellt `main.py` Tabellen, aber bestehende DBs können via `ALTER TABLE` erweitert werden (siehe Runbook weiter unten).

## API Endpunkte

Base-URL (lokal): `http://127.0.0.1:8000`

1) GET /calendar
- Params: `user_id` (int)
- Response: 200 JSON Array von CalendarEvent-Objekten
- Beispiel: `GET /calendar?user_id=2`

2) POST /calendar
- Body (JSON): { user_id, title, description?, start, end, created? }
- Response: 201 Created, zurückgegebenes Event (inkl. id)
- Hinweis: `created` wird gesetzt, falls nicht angegeben.

3) GET /documents
- Params: `user_id` (int)
- Response: 200 JSON Array von Document-Objekten

4) GET /
- Health-Endpoint; einfache Welcome-Nachricht.

Swagger/OpenAPI: `http://127.0.0.1:8000/docs`

## Lokales Setup & Start (Windows / PowerShell)

1) In das Backend-Verzeichnis wechseln:

```powershell
Set-Location -Path "C:\Users\christopherki\Ausbildungstool_Backend"
```

2) Virtuelle Umgebung erstellen (falls noch nicht vorhanden) und aktivieren:

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
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Die Anwendung legt beim ersten Start Tabellen an und seedet Beispiel-Daten, falls die DB leer ist.

## DB-Migration / `created` Spalte

Falls du eine vorhandene `azubi.db` verwendest und die neue Spalte `created` fehlt, kannst du sie per SQLite-CLI (oder DB Browser) hinzufügen:

```powershell
# mit sqlite3 CLI
sqlite3 .\azubi.db "ALTER TABLE calendar_events ADD COLUMN created DATETIME;"
sqlite3 .\azubi.db "UPDATE calendar_events SET created = datetime('now') WHERE created IS NULL;"
```

Alternativ in dev: lösche `azubi.db` und starte das Backend neu — `Base.metadata.create_all()` legt die Tabellen neu an und `seed_db` legt Beispieldaten an.

## Hinweise zur Integration mit Frontend

- Frontend ruft `GET /calendar?user_id=...` und `POST /calendar` auf. Payloads sollten ISO-8601 Datumsstrings für `start`/`end` verwenden (z. B. `2025-11-17T08:00:00Z`).
- CORS ist für die gängigen lokalen Dev-Ports konfiguriert (z. B. `http://127.0.0.1:5173`).
- Auth wird aktuell nicht geprüft — Header `Authorization` wird ignoriert (Frontend kann Mock-JWT senden).

## Troubleshooting

- 500 bei POST → häufigste Ursache: DB-Spalte fehlt (siehe Migration oben).
- Pydantic-Warnung: `orm_mode` → Pydantic v2 empfiehlt `from_attributes = True`. Das ist aktuell nur eine Warnung.
- uvicorn nicht gefunden → sicherstellen, dass die virtuelle Umgebung aktiviert ist oder `python -m uvicorn` verwenden.

## Runbook / Quick Commands

```powershell
# Backend: starten
Set-Location -Path "C:\Users\christopherki\Ausbildungstool_Backend"
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# DB: Backup
Copy-Item .\azubi.db .\azubi.db.bak -Force

# DB: Migration (falls nötig)
sqlite3 .\azubi.db "ALTER TABLE calendar_events ADD COLUMN created DATETIME;"
```

## Weiteres / Empfehlungen

- Für produktive Nutzung: verwende eine richtige DB (Postgres), setze Alembic für Migrationen und implementiere Auth (OAuth2/JWT).
- Pflege `requirements.txt` und pinne Versionen für reproduzierbare Builds.

Wenn du willst, kann ich diese README noch um zusätzliche Abschnitte ergänzen (z. B. Tests, CI/CD, Deployment-Schritte).

