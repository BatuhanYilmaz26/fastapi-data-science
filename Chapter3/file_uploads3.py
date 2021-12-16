from typing import List
from fastapi import FastAPI, File, UploadFile

# You can even accept multiple files by type hinting the argument as a list of UploadFile:

app = FastAPI()

@app.post("/files")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    return [
        {"file_name": file.filename, "content_type": file.content_type}
        for file in files
        ]

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn file_uploads3:app

# To upload several files with HTTPie, simply repeat the argument. 
# It should appear as follows:
# $ http --form POST http://localhost:8000/files files@./assets/cat.jpg files@./assets/cat.jpg