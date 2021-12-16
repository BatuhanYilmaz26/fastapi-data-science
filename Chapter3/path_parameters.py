from fastapi import FastAPI
from enum import Enum

# The API path is the main thing that the end user will interact with. 
# Therefore, it's a good spot for dynamic parameters.
# A typical example is to put the unique identifier of an object we want to retrieve, such as /users/123.
class UserType(str, Enum):
    STANDARD = "standard"
    ADMIN = "admin"

app = FastAPI()

@app.get("/users/{type}/{id}")
async def get_user(type: UserType, id: int):
    return {"type": type, "id": id}

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn path_parameters:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# http http://localhost:8000/users/standard/26 