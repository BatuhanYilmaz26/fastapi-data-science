from fastapi import FastAPI, Header

# Headers and cookies
# Besides the URL and the body, another major part of the HTTP request are the headers.
# They contain all sorts of metadata that can be useful when handling requests. 
# A common usage is to use them for authentication, for example, via the famous cookies.
# Once again, retrieving them in FastAPI only involves a type hint and a parameter function.
# Let's take a look at a simple example where we want to retrieve a header named Hello:

app = FastAPI()

@app.get("/")
async def get_header(hello: str = Header(...)):
    return {"hello": hello}

# Here, you can see that we simply have to use the Header function as a default value for the hello argument. 
# The name of the argument determines the key of the header that we want to retrieve. 
# Let's see this in action:

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn headers_cookies:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http GET http://localhost:8000 'Hello: World'

# FastAPI was able to retrieve the header value. 
# Since there was no default value specified (we put in an ellipsis), the header is REQUIRED. 
# If it's missing, once again, you'll get a 422 status error response.