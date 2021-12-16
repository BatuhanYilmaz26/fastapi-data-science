from typing import Optional
from fastapi import FastAPI, Cookie

# One very special case of header is cookies. 
# You could retrieve them by parsing the Cookie header yourself, but that would be a bit tedious. 
# FastAPI provides another parameter function that automatically does it for you.
# The following example simply retrieves a cookie named hello:

app = FastAPI()

@app.get("/")
async def get_cookie(hello: Optional[str] = Cookie(None)):
    return {"hello": hello}

# Notice that we type hinted the argument as Optional, and we set a default value of None to the Cookie function. 
# This way, even if the cookie is not set in the request, FastAPI will proceed and not generate a 422 status error response.

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn headers_cookies2:app

# Now, let's make a very simple request. We'll keep the default user agent of HTTPie to see what happens:
# $ http -v GET http://localhost:8000