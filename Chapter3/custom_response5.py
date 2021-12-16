from fastapi import FastAPI, Response

# Custom responses
# Finally, if you really have a case that's not covered by the provided classes, you always have the option 
    # to use the Response class to build exactly what you need. 
# With this class, you can set everything, including the body content and the headers.
# The following example shows you how to return an XML response:

app = FastAPI()

@app.get("/xml")
async def get_xml():
    content = """<?xml version="1.0" encoding="UTF-8"?>
        <Hello>World</Hello>
    """
    return Response(content=content, media_type="application/xml")

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn custom_response5:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http GET http://localhost:8000/xml