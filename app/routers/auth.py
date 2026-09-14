# APIRouter: lets a set of path operations be defined separately and plugged into the main app
from fastapi import APIRouter, Depends, status, HTTPException, Response

# OAuth2PasswordRequestForm: parses a standard OAuth2 login form (username + password fields)
from fastapi.security import OAuth2PasswordRequestForm

# Session: type hint for a SQLAlchemy database session object
from sqlalchemy.orm import Session

# models, schemas, utils: ORM models, request/response schemas, and the password-hashing helpers
from .. import models, schemas, utils

# get_db: dependency that yields a database session
from ..database import get_db

# create_access_token: builds a signed JWT for a successfully authenticated user
from ..oauth2 import create_access_token

# router: collects the auth-related path operations defined in this file
router = APIRouter(tags=["Authentication"])


# POST /login: verifies a user's email + password against the users table, returns a JWT if valid
# user_credentials is parsed from form data (not JSON); its "username" field holds the email
@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Look up the user by the email they submitted (OAuth2PasswordRequestForm names this field "username")
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    # If no user has that email, credentials are invalid
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Compare the submitted plaintext password against the stored bcrypt hash
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Password matched: issue a JWT embedding the user's id, so future requests can identify them
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
