from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"hello": "world"}

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn first_endpoint:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# http http://localhost:8000