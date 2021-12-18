from os import stat
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Updating an instance with a partial one
# In some situations, you'll want to allow partial updates. 
# In other words, you'll allow the end user to only send the fields 
    # they want to change to your API and omit the ones that shouldn't change. 
# This is the usual way of implementing a PATCH endpoint.

# To do this, you would first need a special Pydantic model with all the fields 
    # marked as optional so that no error is raised when a field is missing. 
# Let's see what this looks like with our Post example, as follows:


class PostBase(BaseModel):
    title: str
    content: str


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


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

# We are now able to implement an endpoint that will accept a subset of our Post fields.
# Since it's an update, we'll retrieve an existing post in the database thanks to its ID. 
# Then, we'll have to find a way to only update the fields in the payload and keep the others untouched. 
# Fortunately, Pydantic once again has this covered, with handy methods and options.

# Let's see how the implementation of such an endpoint could look in the following example:

@app.patch("/posts/{id}", response_model=PostPublic)
async def partial_update(id: int, post_update: PostPartialUpdate):
    try:
        post_db = db.posts[id]

        updated_fields = post_update.dict(exclude_unset=True)
        updated_post = post_db.copy(update=updated_fields)

        db.posts[id] = updated_post
        return updated_post
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

# Our path operation function takes two arguments: the id property (from the path), and a PostPartialUpdate instance (from the body).

# The first thing to do is to check if this id property exists in the database. 
# Since we use a dictionary for our dummy database, accessing a non-existing key will raise a KeyError error. 
# If this happens, we simply raise an HTTPException exception with the 404 status code.

# Now for the interesting part: updating the existing object. 
# You see that the first thing we do is transform PostPartialUpdate into a dictionary with the dict method. 
# This time, however, we set the exclude_unset argument to True. 
# The effect of this is that Pydantic won't output the fields that were not provided in the resulting dictionary: 
    # we only get the fields that the user did send in the payload.

# Then, on our existing post_db database instance, we call the copy method. 
# This is a useful method to clone a Pydantic object into another instance. 
# The nice thing about this method is that it even accepts an update argument. 
# This argument expects a dictionary with all the fields that should be updated during the copy: 
    # that's exactly what we want to do with our updated_fields dictionary!

# And that's it! We now have an updated post instance with only the changes required in the payload. 
# You'll probably use the exclude_unset argument and the copy method quite often while developing with FastAPI, 
    # so be sure to keep them in mind—they'll make your life easier!