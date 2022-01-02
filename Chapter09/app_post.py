from fastapi import FastAPI, status
from pydantic import BaseModel

# Writing tests for POST endpoints
# Testing a POST endpoint is not very different from what we've seen earlier. 
# The difference is that we'll likely have more cases to check if data validation is working. 
# In the following example, we are implementing a POST endpoint that accepts a Person model in the body:

app = FastAPI()


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int


@app.post("/persons", status_code=status.HTTP_201_CREATED)
async def create_person(person: Person):
    return person

# An interesting test could be to ensure that an error is raised if some fields are missing in the request payload. 
# In the next example, we'll write two tests: one with an invalid payload and another with a valid one: --> app_post_test.py