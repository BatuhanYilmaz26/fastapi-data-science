from fastapi import FastAPI
from pydantic import BaseModel

# The response model
# With FastAPI, the main use case is to directly return a pydantic model that automatically gets turned into properly formatted JSON.
# However, quite often, you'll find that there are some differences between the input data, 
    # the data you store in your database, and the data you want to show to the end user.
# For instance, perhaps some fields are private or only for internal use, or perhaps some fields are only useful 
    # during the creation process and then discarded afterward.

# Now, let's consider a simple example. Assume you have a database containing blog posts.
# Those blog posts have several properties, such as a title, content, or creation date.
# Additionally, you store the number of views of each one, but you don't want the end user to see any of this.
# You could take the standard approach as follows:

class Post(BaseModel):
    title: str
    nb_views: int

class PublicPost(BaseModel):
    title: str

app = FastAPI()

# Dummy database
posts = {
    1: Post(title="Hello", nb_views=100),
}

@app.get("/posts/{id}", response_model=PublicPost)
async def get_post(id: int):
    return posts[id]

# The only change is to add the response_model option as a keyword argument for the path decorator.

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn response_path_parameters4:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http GET http://localhost:8000/posts/1

# The nb_views property is no longer there! 
# Thanks to the response_model option, FastAPI automatically converted our Post instance into a PublicPost instance before serializing it. 
# Now our private data is safe!