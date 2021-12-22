from datetime import datetime
from enum import auto
from typing import List, Optional

import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy.sql.expression import null

# Adding relationships 
# As we mentioned at the beginning of this chapter, relational databases are all about data and its relationships. 
# Quite often, you'll need to create entities that are linked to others.

# For example, in a blog application, comments are linked to the post they relate to. 
# In this section, we'll examine how you can set up such relationships with SQLAlchemy. 
# Since it's very close to SQL, you'll discover that there's nothing truly surprising about it.


class CommentBase(BaseModel):
    post_id: int
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str


class CommentCreate(CommentBase):
    pass


class CommentDB(CommentBase):
    id: int


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    id: int


class PostPublic(PostDB):
    comments: List[CommentDB]


# Here, you can see that we added a comments attribute, which is a list of CommentDB.
# Indeed, in a REST API, there are some cases where it makes sense to automatically retrieve the associated objects of an entity. 
# Here, it'll be convenient to get the comments of a post in a single request. 
# We'll use this model when getting a single post to serialize the comments along with the post data.

metadata = sqlalchemy.MetaData()

posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("publication_date", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text(), nullable=False),
)

# First, we need to define the table for the comments, which has a foreign key toward the posts table. 
# You can view its definition in the following example:

comments = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("publication_date", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text(), nullable=False),
)

# The important point here is the post_id column, which is of the ForeignKey type.
# This is a special type that tells SQLAlchemy to automatically handle the type of the column and the associated constraint. 
# We simply have to give the table and column names it refers to. 
# Note that we can also specify the ON DELETE action.
# Use the ON DELETE CASCADE option to specify whether you want rows deleted in a child table 
    # when corresponding rows are deleted in the parent table.

# Next, we'll implement an endpoint to create a new comment. 
# This will be shown in the next example. --> app.py