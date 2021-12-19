from typing import Dict, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel

# Get an object or raise a 404 error
# In a REST API, you'll typically have endpoints to get, update, and delete a single object given its identifier in the path. 
# On each one, you'll likely have the same logic: try to retrieve this object in the database or raise an error 404 if it doesn't exist. 
# That's a perfect use case for a dependency! 
# In the following example, you'll see how to implement it:


class Post(BaseModel):
    id: int
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]


class DummyDatabase:
    posts: Dict[int, Post] = {}


db = DummyDatabase()
db.posts = {
    1: Post(id=1, title="Post 1", content="Content 1"),
    2: Post(id=2, title="Post 2", content="Content 2"),
    3: Post(id=3, title="Post 3", content="Content 3"),
}

app = FastAPI()

async def get_post_or_404(id: int) -> Post:
    try:
        return db.posts[id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# The dependency definition is simple: it takes in an argument the ID of the post we want to retrieve. 
# It will be pulled from the corresponding path parameter. 
# Then, we check whether it exists in our dummy dictionary database: if it does, we return it, 
    # otherwise, we raise an HTTPException with the status code 404.
# That's the key takeaway of this example: you can raise errors in your dependencies. 
# It's extremely useful to check for some pre-conditions before your endpoint logic is executed.
# Another typical example for this is authentication: if the endpoint requires a user to be authenticated, 
    # we can raise a 401 error in the dependency by checking for the token or the cookie.

# Now, we can use this dependency in each of our API endpoints, as you can see in the following example:

@app.get("/posts/{id}")
async def get(post: Post = Depends(get_post_or_404)):
    return post

@app.patch("/posts/{id}")
async def update(post_update: PostUpdate, post: Post = Depends(get_post_or_404)):
    updated_post = post.copy(update=post_update.dict())
    db.posts[post.id] = updated_post
    return updated_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(post: Post = Depends(get_post_or_404)):
    db.posts.pop(post.id)

# As you can see, we just had to define the post argument and use the Depends function on our get_post_or_404 dependency. 
# Then, within the path operation logic, we are guaranteed to have our post object at hand and 
    # we can focus on our core logic, which is now very concise. 
# The get endpoint, for example, just has to return the object.

# In this case, the only point of attention is to not forget the ID parameter in the path of those endpoints. 
# According to the rules of FastAPI, if you don't set this parameter in the path, it will automatically 
    # be regarded as a query parameter, which is not what we want here.

# That's all for the function dependencies. 
# As we said, those are the main building blocks in a FastAPI project. 
# In some cases, however, you'll need to have some parameters on those dependencies, for example, with values coming from environment variables. 
# For this, we can define class dependencies. -> class_dependency.py 

# Let's run this example with the following command:
# $ uvicorn function_dependency:app

# Now let's try our endpoint with the following HTTPie command:
# $ http GET "http://localhost:8000/posts/2"