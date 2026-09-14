# APIRouter: lets a set of path operations be defined separately and plugged into the main app
from fastapi import APIRouter, Depends, HTTPException, status

# Session: type hint for a SQLAlchemy database session object
from sqlalchemy.orm import Session

# models: the module defining the User ORM model, mapped to the "users" table
from .. import models

# schemas: the module defining the User Pydantic schemas, used to validate request/response bodies
from .. import schemas

# hash_password: hashes a plaintext password with bcrypt before it's stored
from ..utils import hash_password

# get_db: dependency that yields a database session
from ..database import get_db

# oauth2: the module defining get_current_user, the dependency that requires a valid JWT
from .. import oauth2

# router: collects the user-related path operations defined in this file
router = APIRouter(prefix="/users", tags=["Users"])


# POST /createuser: creates a new user in the users table, with the password hashed, and returns it
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Replace the plaintext password with its bcrypt hash before it ever reaches the database
    user.password = hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GET /getuserdetails/{id}: queries the users table for a single user by id, or 404 if it doesn't exist, via the ORM
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} was not found",
        )
    return user
