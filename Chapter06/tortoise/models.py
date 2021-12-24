from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from tortoise.models import Model
from tortoise import fields

# Creating database models
# The first step is to create the Tortoise model for your entity. 
# This is a Python class whose attributes represent the columns of your table. 
# This class will provide you static methods in which to perform queries, such as retrieving or creating data. 
# Moreover, the actual entities of your database will be instances of this class, giving you access to its data like any other object. 
# Under the hood, the role of Tortoise is to make the link between this Python object and the row in the database. 
# Let's take a look at the definition of our blog post model in the following example:

# We have defined the corresponding Pydantic models for our post entity. 
# They will be used by FastAPI to perform data validation and serialization. 
# As you can see in the following example, we added a Config sub-class and set an attribute called orm_mode:
# This option will allow us to transform an ORM object instance into a Pydantic object instance. 
# This is essential because FastAPI is designed to work with Pydantic models, not ORM models.


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    id: int


class PostTortoise(Model):
    id = fields.IntField(pk=True, generated=True)
    publication_date = fields.DatetimeField(null=False)
    title = fields.CharField(max_length=255, null=False)
    content = fields.TextField(null=False)

    class Meta:
        table = "posts"


# Our model is a class that is inheriting from the tortoise.models.Model base class.
# Each field (or column) is an instance of a class corresponding to the type of the field. 
# Each one has its own set of arguments to finely tune the definition in the database.
# For example, our id field is a primary key that is automatically generated. 
# We won't go through every field's class, but you can find the complete list 
    # in the official Tortoise documentation at https://tortoise-orm.readthedocs.io/en/latest/fields.html.
# Notice that we also have a sub-class called Meta, which allows us to set some options for our table. 
# Here, the table attribute allows us to control the name of the table.