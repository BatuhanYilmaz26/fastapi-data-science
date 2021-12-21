from datetime import date, datetime
from typing import Optional
import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy import sql
from sqlalchemy.sql.expression import null

# Creating the table schema
# First, you need to define the SQL schema for your tables: the name, the columns, and their associated types and properties. 
# SQLAlchemy provides a full set of classes and functions to help you in this task. 
# In the following example, you can view the definition of the posts table:


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
    id:  int


metadata = sqlalchemy.MetaData()

posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("publication_date", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text(), nullable=False),
)

# First, we created a MetaData object.
# MetaData is a container object that keeps together many different features of a database (or multiple databases) being described.

# Next, we defined a table using the Table class.
# Its two primary arguments are the table name, then the MetaData object which it will be associated with. 
# The remaining positional arguments are mostly Column objects describing each column.
    # sqlalchemy.Column("column_name", datatype, ...)