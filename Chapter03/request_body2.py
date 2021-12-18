from fastapi import FastAPI
from pydantic import BaseModel

# In this example let's rewrite our previous request_body example using pydantic:

# First, we import BaseModel from pydantic. 
    # This is the base class that every model should inherit from. 
# Then, we define our User class and simply list all of the properties as class properties. 
# Each one of them should have a proper type hint: this is how Pydantic will be able to validate the type of the field.

class User(BaseModel):
    name: str
    age: int

app = FastAPI()

@app.post("/users")
async def create_user(user: User):
    return user

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn request_body2:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# http -v POST http://localhost:8000/users name="John" age=30