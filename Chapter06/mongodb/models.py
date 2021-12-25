from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

# Creating models compatible with MongoDB ID
# There are some difficulties with the identifiers that MongoDB uses to store documents. 
# Indeed, by default, MongoDB assigns every document an _id property that acts as a unique identifier in a collection. 
# This causes two issues:
# • In a Pydantic model, if a property starts with an underscore, it's considered to be private and, thus, is not used as a data field for our model.
# • _id is encoded as a binary object, called ObjectId, instead of a simple integer or string. 
# It's usually represented in the form of a string such as 608d1ee317c3f035100873dc. 
# This type of object is not supported out of the box by Pydantic or FastAPI.
# This is why we'll need some boilerplate code to ensure those identifiers work with Pydantic and FastAPI.


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# In the following example, we have created a MongoBaseModel base class that takes care of defining the id field:

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}

# First, we need to define an id field, which is of type PyObjectId. 
# This is a custom type that has been defined in the preceding code. 
# We won't go into the details of its implementation, but just know that it's a class that makes ObjectId a compatible type for Pydantic. 
# We define this same class as a default factory for this field. 
# Interestingly, that kind of identifier allows us to generate them on the client side, contrary to traditional auto-incremented integers of relational databases, which could be useful in some cases.
# The most interesting argument is alias. 
# It's a Pydantic option allowing us to change the name of the field during serialization. 
# In this example, when we call the dict method on one instance of MongoBaseModel, the identifier will be set on the _id key; this is the name expected by MongoDB. 
# That solves the first issue.

# Then, we add the Config sub-class and set the json_encoders option. 
# By default, Pydantic is completely unaware of our PyObjectId type, so it won't be able to correctly serialize it to JSON. 
# This option allows us to map custom types with a function that will be called to serialize them. 
# Here, we simply transform it into a string (it works because ObjectId implements the __str__ magic method). 
# That solves the second issue for Pydantic.


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
    pass

# Our base model for Pydantic is complete! 
# We can now use it as a base class instead of BaseModel for our actual data models. 
# Notice, however, that the PostPartialUpdate doesn't inherit from it. 
# Indeed, we don't want the id field in this model; otherwise, a PATCH request might be able to replace the ID of the document, which could lead to weird issues.