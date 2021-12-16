from fastapi import FastAPI, Form

# Form Data
# Even if REST APIs work most of the time with JSON, sometimes, you might have to 
    # handle form-encoded data or file uploads, which have been encoded either 
    # as application/x-www-form-urlencoded or multipart/form-data.

app = FastAPI()

@app.post("/users")
async def create_user(name: str = Form(...), age: int = Form(...)):
    return {"name": name, "age": age}

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn form_data:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http -v --form POST http://localhost:8000/users name=John age=30