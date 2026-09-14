# jwt: encodes and decodes JSON Web Tokens; JWTError: raised when a token is invalid, expired, or tampered with
from jose import jwt, JWTError

# datetime, timedelta: used to set the token's expiry time
from datetime import datetime, timedelta

# Depends: declares a dependency; status, HTTPException: build the 401 raised for a bad/missing token
from fastapi import Depends, status, HTTPException

# OAuth2PasswordBearer: reads the "Authorization: Bearer <token>" header and extracts the raw token string
from fastapi.security import OAuth2PasswordBearer

# Session: type hint for a SQLAlchemy database session object
from sqlalchemy.orm import Session

# schemas: the module defining TokenData, the shape of the data decoded from a token's payload
# models: the module defining the User ORM model, mapped to the "users" table
from . import schemas, models

# get_db: dependency that yields a database session
from .database import get_db

# settings: config values loaded from the .env file, instead of hardcoding secrets here
from .config import settings

# oauth2_scheme: tells FastAPI where the token is obtained from (the /login route), for /docs and header parsing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY: signs the token so it can't be forged or tampered with without this key
SECRET_KEY = settings.secret_key

# ALGORITHM: the signing algorithm used to sign/verify the token
ALGORITHM = settings.algorithm

# ACCESS_TOKEN_EXPIRE_MINUTES: how long a token stays valid after being issued
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# create_access_token: builds a signed JWT embedding the given data, with an expiry claim added
def create_access_token(data: dict):
    # Copy the data so the caller's dict isn't mutated by adding "exp" below
    to_encode = data.copy()

    # Compute the expiry timestamp: now + the configured number of minutes
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add the expiry claim to the payload; "exp" is the standard JWT field jose checks
    to_encode.update({"exp": expire})

    # Sign and encode the payload into a JWT string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# verify_access_token: decodes and validates a JWT, raising credentials_exception if it's invalid or expired
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the token; this also checks the signature and the "exp" expiry claim automatically
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Pull the user id back out of the payload
        id = payload.get("user_id")
        # If there's no user_id claim, treat the token as invalid
        if id is None:
            raise credentials_exception
        # Wrap the id in the TokenData schema for a consistent return type
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        # Signature mismatch, expired token, or malformed token all land here
        raise credentials_exception

    return token_data


# get_current_user: FastAPI dependency that resolves the Authorization header into the requesting models.User
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # The exception to raise if the token is missing, expired, or otherwise invalid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode the token to get the user's id
    token_data = verify_access_token(token, credentials_exception)

    # Look up the actual user row by that id
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    # If the token's user_id doesn't match any real user (e.g. the account was since deleted), reject it
    if user is None:
        raise credentials_exception

    return user
