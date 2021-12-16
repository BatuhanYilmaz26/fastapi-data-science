from fastapi import FastAPI, status
from pydantic import BaseModel

# Set customized status code

class Post(BaseModel):
    title: str

app = FastAPI()

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn response_path_parameters:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http POST http://localhost:8000/posts title="Hello"

# We have got our 201 status code.
# It's important to understand that this option to override the status code is only useful when everything goes well. 
# Even if your input data was invalid, you would still get a 422 status error response.