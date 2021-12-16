from fastapi import FastAPI, Response, status
from pydantic import BaseModel

# Setting The Status Code Dynamically
# In the Path operation parameters section, we discussed a way to declaratively set the status code of the response. 
# The drawback to this approach is that it'll always be the same no matter what's happening inside.

# Let's assume that we have an endpoint that updates an object in the database or creates it if it doesn't exist. 
# A good approach would be to return a 200 OK status when the object already exists or a 201 Created status when the object has to be created.
# To do this, you can simply set the status_code property on the Response object:

class Post(BaseModel):
    title:str

app = FastAPI()

# Dummy database
posts = {
    1: Post(title="Hello"),
}

@app.put("/posts/{id}")
async def update_or_create_post(id: int, post: Post, response: Response):
    if id not in posts:
        response.status_code = status.HTTP_201_CREATED
    posts[id] = post
    return posts[id]

# First, we check whether the ID in the path exists in the database. 
# If not, we change the status code to 201. 
# Then, we simply assign the post at this ID in the database.

# Let's try with an existing post first:

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn response_parameter3:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http PUT http://localhost:8000/posts/1 title="Updated title"

# The post with an ID of 1 already exists, so we get a 200 status. Now, let's try with a non-existing ID:
# $ http PUT http://localhost:8000/posts/2 title="Updated title"
# We get a 201 status!

# Now you have a way to dynamically set the status code in your logic. 
# Bear in mind, though, that they won't be detected by the automatic documentation. 
# Therefore, they won't appear as a possible response status code in it.

# You might be tempted to use this approach to set error status codes, such as 400 Bad Request or 404 Not Found. 
# In fact, you shouldn't do that. FastAPI provides a dedicated way to do this: HTTPException.