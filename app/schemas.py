# BaseModel: base class for defining request/response schemas; ConfigDict: lets a schema read from ORM objects
# EmailStr: validates that a field is a syntactically correct email address
from pydantic import BaseModel, ConfigDict, EmailStr

# datetime: type hint for the created_at timestamp column
from datetime import datetime

# Optional: marks a schema field as allowed to be its type or None; Literal: restricts a field to specific values
from typing import Optional, Literal


# Schema for the shape of a post; FastAPI validates incoming JSON against this
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# Schema for the fields a client must send to create a post; identical to PostBase for now
class PostCreate(PostBase):
    pass




# Schema for the fields returned about a user; deliberately excludes password
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # from_attributes: lets this schema be built from an object's attributes (e.g. an ORM object), not just a dict
    model_config = ConfigDict(from_attributes=True)

# Schema for the shape of a post sent back in a response, built from a models.Post ORM object
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # from_attributes: lets this schema be built from an object's attributes (e.g. an ORM object), not just a dict
    model_config = ConfigDict(from_attributes=True)


# Schema for a post response paired with its vote count; built from a (Post, votes) query row
class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    model_config = ConfigDict(from_attributes=True)


# Schema for the fields a client must send to register a new user
class UserCreate(BaseModel):
    email: EmailStr
    password: str



# Schema for the fields a client must send to log in (kept for reference; /login now uses OAuth2PasswordRequestForm instead)
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for the response sent back after a successful login
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema for the data decoded out of a JWT's payload
class TokenData(BaseModel):
    id: Optional[str] = None


# Schema for the fields a client sends to cast or remove a vote; dir=1 adds a vote, dir=0 removes it
class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
