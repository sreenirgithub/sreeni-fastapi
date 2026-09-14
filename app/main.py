# FastAPI: core class that creates the application instance
from fastapi import FastAPI

# CORSMiddleware: lets browsers on other origins (different host/port) call this API
from fastapi.middleware.cors import CORSMiddleware

# models: the module defining the ORM models, mapped to their tables
from . import models

# engine: the SQLAlchemy engine connected to the database
from .database import engine

# posts, users, auth, vote: router modules, each collecting a related group of path operations
from .routers import posts, users, auth, vote

# Bind the ORM models' metadata to engine, creating any tables that don't already exist in the database
# models.Base.metadata.create_all(bind=engine)

# The FastAPI application instance that uvicorn runs
app = FastAPI()

# origins: which frontend origins (scheme+host+port) are allowed to call this API from a browser
origins = ["*"]

# Register CORS middleware; "*" allows any origin, which is convenient for learning/dev but not for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Plug the posts router's path operations into the main app
app.include_router(posts.router)

# Plug the users router's path operations into the main app
app.include_router(users.router)

# Plug the auth router's path operations into the main app
app.include_router(auth.router)

# Plug the vote router's path operations into the main app
app.include_router(vote.router)


# GET /helloworld: basic welcome route
@app.get("/helloworld")
def root():
    return {"message": "Welcome to the fastapi course using Claude Code"}
