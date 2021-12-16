from fastapi import FastAPI
from pydantic import BaseModel

# Sometimes, you might find that you have several objects that you wish to send in the same payload all at once. 
    # For example, both user and company. 
# In this scenario, you can simply add several arguments that have been type hinted by a pydantic model, 
# and FastAPI will automatically understand that there are several objects.

class User(BaseModel):
    name: str
    age: int


class Company(BaseModel):
    name: str

app = FastAPI()

@app.post("/users")
async def create_user(user: User, company: Company):
    return {"user": user, "company": company}

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn request_body3:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# For more complex JSON structures, it's advised that you pipe a formatted JSON into HTTPie rather than use parameters. 
    # Let's try this as follows:
# $ echo '{"user": {"name": "John", "age": 30}, "company":{"name": "ACME"}}' | http POST http://localhost:8000/users