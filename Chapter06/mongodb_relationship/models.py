from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


# Nesting documents
# At the beginning of this chapter, we mentioned that document-based databases, contrary to relational databases, aim to store all the data related to an entity in a single document.
# In our current example, if we wish to store the comments along with the post, we simply have to add a list containing information regarding each comment.
# In this section, we'll implement this behavior. 
# You should see that the functioning of MongoDB makes it very easy and straightforward.

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class CommentBase(BaseModel):
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str


class CommentCreate(CommentBase):
    pass


class CommentDB(CommentBase):
    pass


class PostBase(MongoBaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    comments: List[CommentDB] = Field(default_factory=list)

# This field is simply a list of CommentDB. 
# Notice here that we use the list function as the default factory for this attribute. 
# This instantiates an empty list by default when we create a PostDB without setting any comments.