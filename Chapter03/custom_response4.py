from os import path
from fastapi import FastAPI
from fastapi.responses import FileResponse

# Serving a file
# Now, let's examine how FileResponse works. 
# This will be useful if you wish to propose some files to download. 
# This response class will automatically take care of opening the file on disk and streaming the bytes along with the proper HTTP headers.

# For this class to work, first, you'll need another extra dependency, aiofiles:
# Then, we just need to return an instance of FileResponse with the path of the file we want to serve as the first argument:

# Let's take a look at how we can use an endpoint to download a picture of a cat.

app = FastAPI()

@app.get("/cat")
async def get_cat():
    root_directory = path.dirname(path.dirname(__file__))
    picture_path = path.join(root_directory, "assets", "cat.jpg")
    return FileResponse(picture_path)

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn custom_response4:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http GET http://localhost:8000/cat

# As you can see, we have the right Content-Length and Content-Type headers for our image. 
# The response even sets the Etag and Last-Modified headers so that the browser can properly cache the resource. 
# HTTPie doesn't show the binary data in the body; however, if you open the endpoint in your browser, you'll see the cat appear!
    # http://localhost:8000/cat  (go through this link in your browser)