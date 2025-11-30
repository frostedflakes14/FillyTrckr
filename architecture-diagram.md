# FillyTrckr Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          User's Browser                                 │
│                     (Home Network: 192.168.0.x)                         │
└────────────────────┬────────────────────────────┬───────────────────────┘
                     │                            │
                     │ HTTP                       │ HTTP
                     │ Port: 3000                 │ Port: 8000
                     │                            │
                     ▼                            ▼
    ┌────────────────────────────┐  ┌────────────────────────────────────┐
    │                            │  │                                    │
    │   React/Angular Frontend   │  │    Reverse Proxy                   │
    │        Container           │  │    (nginx/traefik)                 │
    │                            │  │    For external API access         │
    │  - Dashboard/Table View    │  │                                    │
    │  - Add/Edit Fillys         │  └─────────────┬──────────────────────┘
    │  - Filter/Search/Sort      │                │
    │                            │                │
    └────────────┬───────────────┘                │
                 │                                │
                 │ REST API Calls                 │
                 │ (Container Name: backend)      │
                 │                                │
                 └─────────────┬──────────────────┘
                               │
                               ▼
              ┌─────────────────────────────────────────┐
              │                                         │
              │      FastAPI Backend Container          │
              │           (Python)                      │
              │                                         │
              │  - REST API Endpoints                   │
              │  - SQLAlchemy ORM Models                │
              │  - Business Logic                       │
              │  - Built-in Swagger UI (/docs)          │
              │  - Built-in ReDoc (/redoc)              │
              │                                         │
              │  Port: 8000 (internal)                  │
              │  Container Name: backend                │
              │                                         │
              └──────────────┬──────────────────────────┘
                             │
                             │ SQL Queries
                             │ PostgreSQL Protocol
                             │ (Container Name: postgres)
                             │
                             ▼
              ┌─────────────────────────────────────────┐
              │                                         │
              │     PostgreSQL Database Container       │
              │                                         │
              │  Tables:                                │
              │  - filly_rolls                          │
              │  - filly_types                          │
              │  - filly_colors                         │
              │  - filly_brands                         │
              │  - filly_subtypes                       │
              │                                         │
              │  Port: 5432 (internal only)             │
              │  Container Name: postgres               │
              │                                         │
              └──────────────┬──────────────────────────┘
                             │
                             │ Persistent Storage
                             │
                             ▼
              ┌─────────────────────────────────────────┐
              │      Docker Volume: postgres_data       │
              │       (Database Persistence)            │
              └─────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    Docker Compose / Portainer Stack                     │
│                                                                         │
│  Network: fillytrckr_network (bridge)                                   │
│                                                                         │
│  Services:                                                              │
│    - frontend (React/Angular)                                           │
│    - backend (FastAPI)                                                  │
│    - postgres (PostgreSQL)                                              │
│                                                                         │
│  Volumes:                                                               │
│    - postgres_data                                                      │
│    - Optional: frontend_build (for compiled assets)                     │
│    - Optional: backend_logs (for application logs)                      │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                           CI/CD Pipeline                                │
│                                                                         │
│  Build Scripts (Windows Batch):                                         │
│    - build-frontend.bat                                                 │
│    - build-backend.bat                                                  │
│    - build-all.bat                                                      │
│                                                                         │
│  Process:                                                               │
│    1. Build Docker Image                                                │
│    2. Tag Image                                                         │
│    3. Push to 192.168.0.xx:5000 (Self-hosted Docker Registry)          │
│                                                                         │
│  Image Names:                                                           │
│    - 192.168.0.xx:5000/fillytrckr-frontend:latest                      │
│    - 192.168.0.xx:5000/fillytrckr-backend:latest                       │
└─────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                            Data Flow Example
═══════════════════════════════════════════════════════════════════════════

User Action: "Add new PLA spool"
  │
  ├─► Frontend: User fills form with filly characteristics
  │
  ├─► Frontend: POST request to http://backend:8000/api/v1/filly
  │
  ├─► Backend: Validates data, creates SQLAlchemy model
  │
  ├─► Backend: Inserts into postgres.filly_rolls table
  │
  ├─► PostgreSQL: Commits transaction, returns success
  │
  ├─► Backend: Returns JSON response with created filly data
  │
  └─► Frontend: Updates table view with new row


═══════════════════════════════════════════════════════════════════════════
                          Container Communication
═══════════════════════════════════════════════════════════════════════════

Frontend Container:
  - Serves static files (HTML/CSS/JS)
  - Makes API calls to: http://backend:8000/api/v1/*

Backend Container:
  - Connects to database: postgresql://postgres:5432/fillytrckr
  - Exposes REST API on port 8000
  - Swagger UI available at: http://backend:8000/docs

PostgreSQL Container:
  - Listens on port 5432 (internal only)
  - Data persisted in postgres_data volume


═══════════════════════════════════════════════════════════════════════════
                              Port Mapping
═══════════════════════════════════════════════════════════════════════════

Host Machine (192.168.0.x)  →  Container
  3000                      →  frontend:3000 (or 80)
  8000                      →  backend:8000
  5431                      →  postgres:5432


═══════════════════════════════════════════════════════════════════════════
                          Technology Stack Summary
═══════════════════════════════════════════════════════════════════════════

Frontend:
  - Framework: React or Angular
  - Language: TypeScript/JavaScript
  - Container: Node-based image or nginx serving static files

Backend:
  - Framework: FastAPI
  - Language: Python 3.11+
  - ORM: SQLAlchemy
  - API Docs: Built-in Swagger UI & ReDoc
  - Container: Python slim image

Database:
  - Database: PostgreSQL 15+
  - Container: Official postgres image

Orchestration:
  - Docker Compose / Portainer Stack
  - Self-hosted Docker Registry: 192.168.0.xx:5000


═══════════════════════════════════════════════════════════════════════════
                          Security Considerations
═══════════════════════════════════════════════════════════════════════════

✓ No authentication required (home network only)
✓ PostgreSQL port NOT exposed to host (internal only)
✓ Backend API can be exposed via reverse proxy for future integrations
✓ Database credentials stored in environment variables
✓ No external internet exposure
