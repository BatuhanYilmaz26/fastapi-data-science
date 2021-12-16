from fastapi import FastAPI, Response

# The Response Parameter
# The body and status code are not the only interesting parts of an HTTP response.
# Sometimes, it might be useful to return some custom headers or set cookies. 
# This can be done dynamically using FastAPI directly within the path operation logic. 
# How so? By injecting the Response object as an argument of the path operation function.

# Setting headers
# As usual, this only involves setting the proper type hinting to the argument. 
# The following example shows you how to set a custom header:

app = FastAPI()

@app.get("/")
async def custom_header(response: Response):
    response.headers["Custom-Header"] = "Custom-Header-Value"
    return {"hello": "world"}

# The Response object gives you access to a set of properties, including headers. 
# It's a simple dictionary where the key is the name of the header, and the value is its associated value. 
# Therefore, it's relatively straightforward to set your own custom header.

# Also, notice that you don't have to return the Response object. 
# You can still return JSON-encodable data and FastAPI will take care of forming a proper response, including the headers you've set. 
# Therefore, the response_model and status_code options we discussed in the Path operation parameters section are still honored.

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn response_parameter:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http GET http://localhost:8000

# Our custom header is part of the response.
# As we mentioned earlier, the good thing about this approach is that it's within your path operation logic. 
# That means you can dynamically set headers depending on what's happening in your business logic.