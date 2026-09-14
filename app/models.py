# Column, Integer, String, Boolean, TIMESTAMP: SQLAlchemy types used to define table columns
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP

# text: lets a column default be a raw SQL expression, e.g. the database's own now() function
from sqlalchemy.sql.expression import text

# relationship: lets an ORM model access a related row/table through a Python attribute
from sqlalchemy.orm import relationship

# Base: the declarative base class this model must subclass so SQLAlchemy can map it to a table
from .database import Base


# Post: ORM model mapping to the "posts" table, mirroring the Post schema and raw SQL used in main.py
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    # owner_id: foreign key referencing users.id; ON DELETE CASCADE removes a user's posts if they're deleted
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")


# User: ORM model mapping to the "users" table, for managing registered users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# Vote: ORM model mapping to the "votes" table, a many-to-many link between users and posts
class Vote(Base):
    __tablename__ = "votes"

    # Composite primary key (user_id, post_id): the pair together must be unique, so one user
    # can vote on a given post at most once. ON DELETE CASCADE removes a vote if either side is deleted.
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
