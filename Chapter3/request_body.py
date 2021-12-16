from fastapi import FastAPI, Body

# The body is the part of the HTTP request that contains raw data, representing documents, files, or form submissions. 
# In a REST API, it's usually encoded in JSON and used to create structured objects in a database.
# For the simplest cases, retrieving data from the body works exactly like query parameters.
# The only difference is that you always have to use the Body function; otherwise, FastAPI will look for it inside the query parameters by default.

# Let's explore a simple example where we want to post some user data:
app = FastAPI()

@app.post("/users")
async def create_user(name: str = Body(...), age: int = Body(...)):
    return {"name": name, "age": age}

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn request_body:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# http -v POST http://localhost:8000/users name="John" age=30