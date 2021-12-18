from fastapi import FastAPI, status
from pydantic import BaseModel

# Another interesting scenario for this option is when you have nothing to return, such as when you typically delete an object. 
# In this case, the 204 No content status code is a good fit. 
# In the following example, we implement a simple DELETE endpoint that sets this response status code:

class Post(BaseModel):
    title: str

app = FastAPI()

# Dummy database
posts = {
    1: Post(title="Hello", nb_views=100),
}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    posts.pop(id, None)
    return None