from fastapi import FastAPI, Request

# The Request Object
# Sometimes, you might find that you need to access a raw request object with all of the data associated with it. 
# That's possible. 
# Simply declare an argument on your path operation function type hinted with the Request class:

app = FastAPI()

@app.get("/")
async def get_request_object(request: Request):
    return {"path": request.url.path}

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn request_object:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http GET http://localhost:8000