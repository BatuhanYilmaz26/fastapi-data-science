from fastapi import FastAPI
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    nb_views: int

app = FastAPI()

#  Dummy database
posts = {
    1: Post(title="Hello", nb_views=100),
}

@app.get("/posts/{id}")
async def get_post(id: int):
    return posts[id]

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn response_path_parameters3:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http GET http://localhost:8000/posts/1

# The nb_views property is in the output. 
    # However, we don't want this. 
# This is exactly what the response_model option is for: to specify another model that only outputs the properties we want. 
# First, let's define another pydantic model with only the title property:
    # This will be demonstrated in the next exercise (response_path_parameters4.py).