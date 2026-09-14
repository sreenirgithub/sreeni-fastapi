# FastAPI Learning Project

Following freeCodeCamp's "Python API Development - Comprehensive Course for Beginners"
(https://www.youtube.com/watch?v=0sOvCWFmrtA). Goal: build a Reddit/Pinterest-style
"social media" posts API step by step, learning FastAPI, SQLAlchemy, auth, and
deployment along the way.

## How to use this file
- Work through stages in order. Each stage builds on the last.
- Mark a stage `[x]` when its code is working and understood, not just written.
- When resuming a session, check here first to see the current stage.
- Add short notes under a stage if something in the video didn't match reality
  (library version changes, deprecated APIs, etc.) so we don't relearn it twice.

## Progress

- [x] Stage 0 — Environment setup
  - Python virtual env, install `fastapi`, `uvicorn`
  - Install Postman (or use `/docs` Swagger UI instead)
  - Verify `uvicorn app.main:app --reload` runs
  - Note: `python`/`py` are not on PATH in this shell (Python 3.14.4 installed
    at `C:\Users\User\AppData\Local\Python\pythoncore-3.14-64`). Always invoke
    via the venv directly: `.\.venv\Scripts\python.exe` /
    `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`.

- [~] Stage 1 — First FastAPI app (in progress)
  - Basic app instance, one GET route (`/helloworld`) — done (`app/main.py`)
  - Note: earlier progress notes claimed `/posts/{id}`, `/posts/latest`
    (route-ordering gotcha), and POST with raw dict body were done — they
    were not actually present in `app/main.py`. Restarting Stage 1 from the
    current file instead of trying to reconstruct that lost work.
  - Still to do: GET path operations incl. path params (`/posts/{id}`),
    route-ordering gotcha (`/posts/latest` before `/posts/{id}`), POST with
    raw `dict` body, PUT/DELETE, query parameters
  - Automatic docs at `/docs` and `/redoc` — available, not yet reviewed together

- [ ] Stage 2 — Request/response bodies with Pydantic
  - Pydantic `BaseModel` schemas for request validation
  - In-memory list of posts (no DB yet) — CRUD against the list
  - Response models, status codes, `HTTPException`

- [ ] Stage 3 — PostgreSQL with raw SQL (psycopg2)
  - Install and run PostgreSQL locally
  - Connect via `psycopg2`, cursor, raw SQL CRUD
  - Understand why this is painful (motivates ORM)

- [ ] Stage 4 — SQLAlchemy ORM
  - Engine, `SessionLocal`, declarative `Base`
  - Define `Post` model, dependency-injected DB session
  - Rewrite CRUD endpoints using the ORM

- [ ] Stage 5 — Schemas & config cleanup
  - Split Pydantic schemas from SQLAlchemy models
  - `pydantic-settings` for env vars (DB credentials, secrets)
  - `.env` file, `python-dotenv`

- [ ] Stage 6 — Alembic migrations
  - Init Alembic, autogenerate migrations from models
  - Upgrade/downgrade workflow

- [ ] Stage 7 — Users & password hashing
  - `User` model, registration endpoint
  - Hash passwords with `passlib`/`bcrypt`

- [ ] Stage 8 — JWT authentication
  - Login endpoint issuing JWT (`python-jose`)
  - `OAuth2PasswordBearer`, `get_current_user` dependency
  - Protect routes; users can only modify their own posts

- [ ] Stage 9 — Relationships
  - Foreign key `Post.owner_id -> User.id`
  - SQLAlchemy relationship(), nested response schemas

- [ ] Stage 10 — Votes / likes feature
  - `Vote` association table (many-to-many User<->Post)
  - Query with joins + aggregate like counts

- [ ] Stage 11 — Polish
  - CORS middleware
  - Pagination, search/filter query params
  - Error handling review

- [ ] Stage 12 — Testing
  - `pytest` + `TestClient`
  - Fixtures for test DB, auth token fixtures

- [ ] Stage 13 — Containerization
  - Dockerfile for the app
  - `docker-compose` with app + Postgres

- [ ] Stage 14 — CI/CD & deployment
  - GitHub Actions workflow (test on push)
  - Deploy target (Ubuntu VPS or Heroku-equivalent): Gunicorn + Uvicorn workers,
    Nginx reverse proxy, systemd service — or containerized deploy

## Conventions for this repo
- Project code lives under `app/` once Stage 1 starts (`app/main.py`, `app/models.py`,
  `app/schemas.py`, `app/database.py`, `app/routers/`).
- Use a virtual env (`.venv`); don't install packages globally.
- Prefer the video's structure/naming so it's easy to cross-reference timestamps,
  but call out any place we deliberately diverge (e.g. newer library APIs).
- Comment every line of code with a one-line explanation of what it does (this is
  a learning project — comments are for reinforcing understanding, not just for
  non-obvious logic).
