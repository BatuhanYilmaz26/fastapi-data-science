from fastapi import FastAPI, Header

# Additionally, notice that FastAPI automatically converts the header name to lowercase.
# Besides that, since header names are separated by a hyphen, -, most of the time, it also automatically converts it to snake case. 
# Therefore, it works out of the box with any valid Python variable name. 
# The following example shows this behavior by retrieving the User-Agent header:

app = FastAPI()

@app.get("/")
async def get_header(user_agent: str = Header(...)):
    return {"user_agent": user_agent}

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn headers_cookies2:app

# Now, let's make a very simple request. We'll keep the default user agent of HTTPie to see what happens:
# $ http -v GET http://localhost:8000