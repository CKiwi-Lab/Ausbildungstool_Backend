# Projektantrag — Ausbildungstool

Datum: 27.10.2025

Vorlage: Dieser Antrag orientiert sich an der bereitgestellten Projektantrag-Vorlage und fasst Zielsetzung, Umfang, technische Lösung, API-/DB-Design, Zeitplan und Abnahmebedingungen zusammen.

## 1. Kurzfassung

Ziel dieses Projekts ist die Erstellung eines schlanken Ausbildungs-Management-Tools (Frontend + Backend). Das Backend bietet REST-APIs für Dokumente und Kalenderereignisse, speichert Daten in einer SQLite-Datenbank via SQLAlchemy und verwendet FastAPI. Das Frontend ist eine Vue/Vite-Anwendung, die die APIs nutzt, um z. B. Kalendertermine und Dokumentlisten anzuzeigen und zu bearbeiten.

Der Antrag beschreibt die Anforderungen, geplante Endpunkte, das Datenmodell, den technischen Stack, Meilensteine und Erfolgskriterien.

## 2. Ausgangslage / Motivation

Aktuell existieren zwei Projekteile im Workspace:
- `azubitool_frontend` (Vue 3 + Vite, Tailwind)
- `Ausbildungstool_Backend` (FastAPI, derzeit einfache Endpunkte und eine Beispiel-Datenbank)

Das Frontend benötigt stabile API-Verträge (URLs, Header, Parameter, Beispiel-Responses) und ein persistentes Datenmodell, damit Ansichten wie Kalender, Dokumente und Aufgaben mit echten Daten befüllt werden können. Ziel ist ein minimaler, zuverlässiger Kern mit folgenden Eigenschaften:
- einfache Authentifizierung (später erweiterbar),
- robuste, dokumentierte Endpunkte für Frontend-Integration,
- persistente DB (SQLite) mittels SQLAlchemy,
- einfache CRUD-Funktionen für Kalender und Dokumente.

## 3. Ziele / Erfolgskriterien

Hauptziele:
- Dokumentierte API-Endpunkte für Dokumente und Kalender (GET/POST mindestens),
- Persistente SQLite-Datenbank mit SQLAlchemy-ORM,
- Frontend kann Termine erstellen, anzeigen und die Ansichten mit echten Daten befüllen,
- Lokale Entwicklungs- und Startanleitung (README).

Erfolgskriterien (messbar):
- `GET /calendar?user_id={id}` liefert Ereignisse für `user_id` (Status 200),
- `POST /calendar` legt ein Ereignis in der DB an und ist beim anschließenden `GET` sichtbar,
- `GET /documents?user_id={id}` liefert Dokumente für `user_id`,
- Lokale Startanweisungen führen zu laufender Backend- und Frontend-Instanz.

## 4. Scope (Umfang)

Im ersten Release (MVP) werden implementiert:
- Backend: FastAPI + SQLAlchemy mit folgenden Endpunkten:
  - GET /documents?user_id=int
  - GET /calendar?user_id=int
  - POST /calendar  (Payload: user_id, title, description, start, end)
  - (Optional) POST /documents
- DB: SQLite-Datei (`azubi.db`) mit Tabellen `documents` und `calendar_events`.
- Frontend: Vue-Komponenten anpassen, um Daten von API abzurufen und Termine anzulegen.

Nicht im MVP:
- Vollständige Authentifizierung/Autorisierung (nur Platzhalter/Token später),
- komplexe Filter/Seiten/Benutzerverwaltung,
- Produktionsbereitstellung (Containerisierung, TLS, CI/CD) — optional in Phase 2.

## 5. Technische Lösung / Architektur

Stack:
- Backend: Python 3.11+ (oder 3.14), FastAPI, Uvicorn, SQLAlchemy, Pydantic
- DB: SQLite (lokal) via SQLAlchemy ORM
- Frontend: Vue 3 + Vite, Axios (http client), Tailwind CSS

Kurze Architektur:
- Frontend ruft REST-API-Endpunkte des Backends (z. B. `http://127.0.0.1:8000/calendar`) mit Axios auf.
- Backend verarbeitet Anfragen, führt SQLAlchemy-Queries gegen SQLite aus und liefert JSON-Responses.
- CORS wird für lokale Dev-Ports konfiguriert (z. B. 5173).

## 6. API-Design (Kernendpunkte)

Allgemeine Hinweise:
- Base-URL (lokal): `http://127.0.0.1:8000`
- Header: Standard-HTTP; bei späterer Auth: `Authorization: Bearer <token>`

1) GET /documents
- Beschreibung: Liefert alle Dokumente eines Benutzers.
- Query: `user_id` (int)
- Beispiel: `GET /documents?user_id=1`
- Antwort: 200 OK, JSON-Array of Documents

2) GET /calendar
- Beschreibung: Liefert Kalenderereignisse eines Benutzers.
- Query: `user_id` (int)
- Beispiel: `GET /calendar?user_id=1`
- Antwort: 200 OK, JSON-Array of CalendarEvent

3) POST /calendar
- Beschreibung: Erstellt ein neues Kalenderereignis.
- Body (JSON):
```json
{
  "user_id": 1,
  "title": "Meeting",
  "description": "Team Meeting",
  "start": "2025-10-27T09:00:00Z",
  "end": "2025-10-27T10:00:00Z"
}
```
- Antwort: 201/200 mit dem gespeicherten Event-Objekt (inkl. id)

Hinweis: Das Frontend verwendet `src/api/http.js` (Axios) mit `VITE_API_URL` oder Standard `http://127.0.0.1:8000`.

## 7. Datenmodell (vereinfacht)

Tabelle: documents
- id: Integer, PK
- user_id: Integer, Index
- title: String
- content: Text
- doc_type: String

Tabelle: calendar_events
- id: Integer, PK
- user_id: Integer, Index
- title: String
- description: Text
- start: DateTime
- end: DateTime

Beispiel-Query: `SELECT * FROM documents WHERE user_id = x`

## 8. Entwicklungsplan & Meilensteine

Phase 0 — Vorbereitung (1 Tag)
- Repositorien prüfen, `requirements.txt` und `package.json` validieren, `.gitignore` anwenden.

Phase 1 — MVP Backend (2–3 Tage)
- SQLAlchemy DB-Layer, Models & Schemas
- Implementierung GET/POST-Endpunkte
- CORS und Seed-Daten
- README + API-Dokumentation

Phase 2 — Frontend-Integration (1–2 Tage)
- Frontend-Calls anpassen (CalendarView, DocumentsView)
- Formular/Flows zum Erstellen von Events
- Lokale End-to-End Tests

Phase 3 — Tests, Doku, Puffer (1–2 Tage)
- einfache Unit/Integrationstests,
- Fehlerbehebung, README finalisieren,
- ggf. erste Auth-Implementierung (optional).

Gesamt: 1–2 Kalenderwochen als realistische Schätzung für MVP + Integration (inkl. Puffer)

## 9. Test- & Abnahmebedingungen

Akzeptanztests für Abnahme:
- Backend läuft lokal via `uvicorn main:app --reload`.
- `GET /calendar?user_id=1` liefert vorhandene Seed-Daten (200).
- `POST /calendar` legt ein Event an, welches per `GET` wieder abrufbar ist.
- Frontend (Vite) kann Daten laden und ein neues Event im UI anzeigen.

## 10. Risiken / Annahmen

Risiken:
- SQLite ist für lokale Entwicklung geeignet, aber nicht für hohe Last oder Multi-Write-Szenarien.
- Pydantic- / SQLAlchemy-Versionen können Breaking-Changes haben (Achtung bei Major-Updates).

Annahmen:
- Lokale Entwicklung (Windows) mit Python & Node.js verfügbar.
- Team akzeptiert einfache Token-basierte Auth später.

## 11. Betrieb / Runbook (Kurz)

Backend (PowerShell):
```powershell
Set-Location -Path "C:\Users\christopherki\Ausbildungstool_Backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend (PowerShell):
```powershell
Set-Location -Path "C:\Users\christopherki\azubitool_frontend"
npm install
npm run dev
```

## 12. Deliverables

- Laufendes Backend mit dokumentierten Endpunkten und SQLite-Persistenz.
- Angepasstes Frontend, das Kalendertermine anzeigen und anlegen kann.
- Projekt-README mit Installation, API-Docs, DB-Schema und Testanweisungen.

---

Bei Bedarf kann ich diese Datei noch anpassen (z. B. Zeitplan detaillierter machen, Milestones in JIRA/Trello aufteilen oder zusätzliche Endpunkte spezifizieren). Sag mir, welche Details du noch ergänzt haben möchtest (z. B. formelles Budget, Stakeholder-Liste, oder ein konkreter Sprint-Plan).
