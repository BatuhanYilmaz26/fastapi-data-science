from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

# Building a custom response
# Most of the time, you'll let FastAPI take care of building an HTTP response by simply providing it with some data to serialize. 
# Under the hood, FastAPI uses a subclass of Response, called JSONResponse. 
# Quite predictably, this response class takes care of serializing some data to JSON and adding the correct Content-Type header.
# However, there are other response classes that cover common cases:
# • HTMLResponse: This can be used to return an HTML response.
# • PlainTextResponse: This can be used to return raw text.
# • RedirectResponse: This can be used to make a redirection.
# • StreamingResponse: This can be used to stream a flow of bytes.
# • FileResponse: This can be used to automatically build a proper file response given the path of a file on the local disk.
# You have two ways of using them: either setting the response_class argument on the path decorator or directly returning a response instance.

#Using the response_class argument
# This is the simplest and most straightforward way to return a custom response. 
# Indeed, by doing this, you won't even have to create a class instance: you'll just have to return the data as you do usually for standard JSON responses.
# This is well suited for HTMLResponse and PlainTextResponse:

app = FastAPI()

@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return """
        <html>
            <head>
                <title>Hello World!</title>
            </head>
            <body>
                <h1>Hello World!</h1>
            </body>
        </html>
    """

@app.get("/text", response_class=PlainTextResponse)
async def text():
    return "Hello World!"

# By setting the response_class argument on the decorator, you can change the class that will be used by FastAPI to build the response. 
# Then, you can simply return valid data for this kind of response. 
# Notice that the responses classes are imported through the fastapi.responses module.