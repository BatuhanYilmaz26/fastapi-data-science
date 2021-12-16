from fastapi import FastAPI, File

# File uploads
# Uploading files is a common requirement for web applications, whether this is images or documents. 
# FastAPI provides a parameter function, File, that enables this.
# Let's take a look at a simple example where you can directly retrieve a file as a bytes object:

app = FastAPI()

@app.post("/files")
async def upload_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# We define an argument for the path operation function, file, we add a type of hint, bytes, 
    # and then we use the File function as a default value for this argument. 
# By doing this, FastAPI understands that it will have to retrieve raw data 
    # in a part of the body named file and return it as bytes.
# We simply return the size of this file by calling the len function on this bytes object.
# One drawback to this approach is that the uploaded file is entirely stored in memory. 
# So, while it'll work for small files, it is likely that you'll run into issues for larger files. 
# Besides, manipulating a bytes object is not always convenient for file handling.
    # To fix this problem, FastAPI provides an UploadFile class.
    
# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn file_uploads:app

# Let's upload it on our endpoint using HTTPie. 
# To upload a file, type in the name of the file upload field (here, it is file), 
    # followed by @ and the path of the file you want to upload.
# Don't forget to set the --form option:
# $ http --form POST http://localhost:8000/files file@./assets/cat.jpg