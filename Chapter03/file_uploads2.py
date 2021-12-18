from fastapi import FastAPI, File, UploadFile

# UploadFile class
# This class will store the data in memory up to a certain threshold and, after this, will automatically store it on disk in a temporary location. 
# This allows you to accept much larger files without running out of memory. 
# Furthermore, the exposed object instance exposes useful metadata, such as the content type, and a file-like interface. 
# This means that you can manipulate it as a regular file in Python and that you can feed it to any function that expects a file.
# To use it, you simply have to specify it as a type hint instead of bytes:

app = FastAPI()

@app.post("/files")
async def upload_file(file: UploadFile = File(...)):
    return {"file_name": file.filename, "content_type": file.content_type}

# Notice that, here, we return the filename and content_type properties. 
# The content type is especially useful for checking the type of the uploaded file 
    # and possibly rejecting it if it's not one of the types that you expect.

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn file_uploads2:app

# Here is the result with HTTPie:
# $ http --form POST http://localhost:8000/files file@./assets/cat.jpg