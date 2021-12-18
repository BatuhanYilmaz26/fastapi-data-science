from fastapi import FastAPI, Response

# Setting cookies
# Cookies can also be particularly useful when you want to maintain the user's state within the browser between each of their visits.
# To prompt the browser to save some cookies in your response, you could, of course, build your own Set-Cookie header 
    # and set it in the headers dictionary, just as we saw in the preceding command block. 
# However, since this can be quite tricky to do, the Response object exposes a convenient set_cookie method:

app = FastAPI()

@app.get("/")
async def custom_cookie(response: Response):
    response.set_cookie("cookie-name", "cookie-value", max_age=86400)
    return {"hello": "world"}

# Here, we simply set a cookie, named cookie-name, with the value of cookie-value.
# Of course, if you need to set several cookies, you can call this method several times.
# It'll be valid for 86400 seconds(24 hours) before the browser removes it.

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn response_parameter2:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http GET http://localhost:8000

# Here, you can see that we have a nice Set-Cookie header with all of the properties of our cookie.
# As you may know, cookies have a lot more options than the ones we have shown here; for instance, path, domain, and HTTP-only. 
# The set_cookie method supports all of them. 
# You can read about the full list of options in the official Starlette documentation (since Response is also borrowed from Starlette) at https://www.starlette.io/responses/#set-cookie.