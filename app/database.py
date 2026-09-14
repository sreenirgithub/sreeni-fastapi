# create_engine: builds the connection to the PostgreSQL database
from sqlalchemy import create_engine

# sessionmaker: factory for creating database session objects; declarative_base: base class for ORM models
from sqlalchemy.orm import sessionmaker, declarative_base

# settings: config values loaded from the .env file, instead of hardcoding credentials here
from .config import settings

# Connection string: driver://user:password@host:port/database, built from environment-configured values
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# engine: manages the actual connection pool to the database, using the connection string above
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal: a factory that creates new database session objects bound to this engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: base class that ORM models will subclass so SQLAlchemy can map them to database tables
Base = declarative_base()


# get_db: FastAPI dependency that opens a database session for a request and always closes it afterward
def get_db():
    # Create a new session from the SessionLocal factory
    db = SessionLocal()
    try:
        # Hand the session to the path operation that depends on this function
        yield db
    finally:
        # Close the session once the request is finished, even if an error occurred
        db.close()
