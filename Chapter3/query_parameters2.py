from fastapi import FastAPI
from enum import Enum

class UserFormat(str, Enum):
    SHORT = "short"
    FULL = "full"

app = FastAPI()

@app.get("/users")
async def get_user(format: UserFormat):
    return {"format": format}

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn query_parameters2:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# http "http://localhost:8000/users?format=full"