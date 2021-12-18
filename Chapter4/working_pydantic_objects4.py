from typing import Dict
from fastapi import FastAPI, status
from pydantic import BaseModel

# Creating an instance from a sub-class object
# In the earlier section, Creating model variations with class inheritance, we studied the common pattern of having specific model classes depending on the situation. 
# In particular, you'll have a model dedicated for the creation endpoint, with only the required fields for creation, and a database model with all the fields we want to store.
# Let's take again the Post example, as follows:


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostPublic(PostBase):
    id: int


class PostDB(PostBase):
    id: int
    nb_views: int = 0


class DummyDatabase:
    posts: Dict[int, PostDB] = {}


db = DummyDatabase()

app = FastAPI()

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostPublic)
async def create(post_create: PostCreate):
    new_id = max(db.posts.keys() or (0,)) + 1

    post = PostDB(id=new_id, **post_create.dict())

    db.posts[new_id] = post
    return post

# As you see, the path operation function would give us a valid PostCreate object. 
# Then, we want to transform it into a PostDB object.

# We first determine the missing id property, which is given to us by the database. 
# Here, we use a dummy database based on a dictionary, so we simply take the maximum key already present in the database and increment it. 
# In a real-world situation, this would have been automatically determined by the database.

# The most interesting line here is the PostDB instantiation. 
# You see that we first assign the missing fields by the keyword argument and then unpack the dictionary representation of post_create. 
# As a reminder, the effect of ** in a function call is to transform a dictionary such as {"title": "Foo", "content": "Bar"} into keyword arguments such as this: title="Foo", content="Bar".
# It's a very convenient and dynamic approach to set all the fields we already have into our new model.

# Notice also that we set the response_model argument on the path operation decorator. 
# We already explained this in Chapter 3, Developing a RESTful API with FastAPI, but basically, it prompts FastAPI to build a JSON response with only the fields of PostPublic, 
    # even though we return a PostDB instance at the end of the function.