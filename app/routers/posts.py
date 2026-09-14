# APIRouter: lets a set of path operations be defined separately and plugged into the main app
from fastapi import APIRouter, Depends, HTTPException, Response, status

# Session: type hint for a SQLAlchemy database session object
from sqlalchemy.orm import Session

# List: type hint for a response_model that returns multiple items; Optional: allows a value to be its type or None
from typing import List, Optional

# func: SQL aggregate functions, e.g. func.count(); used to count votes per post
from sqlalchemy import func

# models: the module defining the Post ORM model, mapped to the "posts" table
from .. import models

# schemas: the module defining the Post Pydantic schemas, used to validate request/response bodies
from .. import schemas

# get_db: dependency that yields a database session
from ..database import get_db

# oauth2: the module defining get_current_user, the dependency that requires a valid JWT
from .. import oauth2

# router: collects the post-related path operations defined in this file
router = APIRouter(prefix="/posts",
                   tags=["Posts"])


# GET /getposts: queries and returns up to `limit` rows this user owns in the posts table, with vote counts
@router.get("", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.owner_id == current_user.id)
        .filter(models.Post.content.contains(search))
        .limit(limit).offset(skip)
        .all()
    )
    return results


# GET /getapost/{id}: queries the posts table for a single post owned by this user, or 404, with vote count
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id, models.Post.owner_id == current_user.id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return post


# POST /createpost: inserts a new post into the posts table and returns the inserted row, via the ORM
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    # Stamp the post with the id of whoever is authenticated as the creator
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# DELETE /delete/{id}: deletes a post from the posts table by id, or 404 if it doesn't exist, via the ORM
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    # Only the post's owner may delete it
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# PUT /update/{id}: updates a post's fields in the posts table by id, or 404 if it doesn't exist, via the ORM
@router.put(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse
)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    # Only the post's owner may update it
    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
