from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from tortoise.models import Model
from tortoise import fields


class CommentBase(BaseModel):
    post_id: int
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str

    class Config:
        orm_mode = True

# Here, you can see that we have defined a post_id attribute. 
# This attribute will be used in the request payload to set the post that we want to attach this new comment to. 
# When you provide this attribute to Tortoise, it automatically understands that you are referring to the identifier of the foreign key field, called post.


class CommentCreate(CommentBase):
    pass


class CommentDB(CommentBase):
    id: int


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


# Here, we'll ensure that the comments of a post are returned in the form of a list along with the post data. 
# To do this, we introduce a new Pydantic model, PostPublic. 
# You can view this in the following example:

class PostPublic(PostDB):
    comments: List[CommentDB]

    @validator("comments", pre=True)
    def fetch_comments(cls, v):
        return list(v)

# Predictably, we simply added a comments attribute, which is a list of CommentDB.
# However, here, you can see something unexpected: a validator for this attribute. 
# Earlier, we mentioned that thanks to Tortoise, we can retrieve the comments of a post by simply doing post.comments. 
# This is convenient, but this attribute is not directly a list of data: it's a query set object. 
# If we don't do anything, then, when we try to transform the ORM object into a PostPublic, Pydantic will try to parse this query set and fail. 
# However, calling list on this query set forces it to output the data. 
# That is the purpose of this validator. 
# Notice that we set it with pre=True to make sure it's called before the built-in Pydantic validation.


# Adding relationships
# Now, let's take a look at how to work with relationships. 
# Once again, we'll examine how to implement comments that are linked to posts. 
# One of the main tasks of Tortoise, and ORM in general, is to ease the process of working with related entities, by automatically making the required JOIN queries and instantiating sub-objects. 
# However, once again, there are some things that we need to take care of to make sure everything works smoothly with Pydantic.
# We'll begin by creating a model for our comment entity, as shown in the following example:

class CommentTortoise(Model):
    id = fields.IntField(pk=True, generated=True)
    post = fields.ForeignKeyField(model_name="models.PostTortoise",
        related_name="comments", null=False)
    publication_date = fields.DatetimeField(null=False)
    content = fields.TextField(null=False)

    class Meta:
        table = "comments"

# The main point of interest here is the post field, which is purposely defined as a foreign key. 
# The first argument is the reference to the associated model. 
# Notice that we use the models prefix; this is the same one we defined in the Tortoise configuration that we saw earlier. 
# Additionally, we set the related_name. This is a typical and convenient feature of ORM. 
# By doing this, we'll be able to get all the comments of a given post simply by accessing its comments property. 
# The action of querying the related comments, therefore, becomes completely implicit.


class PostTortoise(Model):
    id = fields.IntField(pk=True, generated=True)
    publication_date = fields.DatetimeField(null=False)
    title = fields.CharField(max_length=255, null=False)
    content = fields.TextField(null=False)

    class Meta:
        table = "posts"