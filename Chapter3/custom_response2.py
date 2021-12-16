from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# Making a redirection
# As mentioned earlier, RedirectResponse is a class that helps you build an HTTP redirection,  which simply is an 
    # HTTP response with a Location header pointing to the new URL and a status code in the 3xx range. 
# It simply expects the URL you wish to redirect to as the first argument:

app = FastAPI()

@app.get("/redirect")
async def redirect():
    return RedirectResponse("/new-url")

# By default, it'll use the 307 Temporary Redirect status code, but you can change this through the status_code argument.