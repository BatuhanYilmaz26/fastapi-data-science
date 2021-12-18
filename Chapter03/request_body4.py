from fastapi import FastAPI, Body
from pydantic import BaseModel

# You can even add singular body values with the Body function.
# This is useful if you wish to have a single property that's not part of any model:

class User(BaseModel):
    name: str
    age: int

app = FastAPI()

@app.post("/users")
async def create_user(user: User, priority: int = Body(..., ge=1, le=3)):
    return {"user": user, "priority": priority}

# The priority property is an integer between 1 and 3, which is expected beside the user object:

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn request_body4:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ echo '{"user": {"name": "John", "age": 30}, "priority": 1}' | http POST http://localhost:8000/users
