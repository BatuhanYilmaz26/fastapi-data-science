from typing import List, Tuple
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

# Implementing an HTTP endpoint to perform face detection on a single image
# Before working with WebSockets, we'll start simple and implement, using FastAPI, a classic HTTP endpoint for accepting image uploads and performing face detection on them. 
# As you'll see, the main difference from the previous example is in how we acquire the image: instead of streaming it from the webcam, we get it from a file upload that we have to convert into an OpenCV image object.
# You can see the whole implementation in the following code:

app = FastAPI()
cascade_classifier = cv2.CascadeClassifier()


class Faces(BaseModel):
    faces: List[Tuple[int, int, int, int]]


@app.post("/face-detection", response_model=Faces)
async def face_detection(image: UploadFile = File(...)) -> Faces:
    data = np.fromfile(image.file, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = cascade_classifier.detectMultiScale(gray)
    if len(faces) > 0:
        faces_output = Faces(faces=faces.tolist())
    else:
        faces_output = Faces(faces=[])
    return faces_output


@app.on_event("startup")
async def startup():
    cascade_classifier.load(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

# As you can see, we start with a rather simple FastAPI application. 
# At the top of the file, we instantiate a CascadeClassifier class. 
# Notice, however, that contrary to the previous example, we load the trained model inside the startup event instead of doing it right away.
# This is for the same reason we explained in Chapter 13, when we loaded our dumped Joblib model: we want to load it only when the application is actually starting, not when we are importing the module.

# Then, we define a face_detection endpoint that expects FileUpload.
# Once we have the file, you can see that we are performing two operations using NumPy and OpenCV. 
# Indeed, the images need to be loaded into a NumPy matrix that is usable by OpenCV.

# If we had a file path, we could have directly used the imread function of OpenCV to load it. 
# Here, we have an UploadFile object that has a file property pointing to a file descriptor. 
# Using NumPy, we can load the binary data into an array of pixels, data. 
# This can be used afterward by the imdecode function to create a proper OpenCV matrix.

# Finally, we can run the prediction using the classifier, as we saw in the previous section (opencv.py).
# Notice that we structure the result into a structured Pydantic model. 
# When OpenCV detects faces, it returns the result as a nested NumPy array. 
# The goal of the tolist method is just to transform it into a standard list of lists.

# You can run this example using the usual Uvicorn command:
# $ uvicorn Chapter14.api:app

# In the code example repository, you'll find a picture of a group of people: https://github.com/PacktPublishing/Building-Data-Science-Applicationswith-FastAPI/blob/main/assets/people.jpg.
# Let's upload it on our endpoint with HTTPie:
# $ http --form POST http://localhost:8000/face-detectionimage@./assets/people.jpg

# The classifier was able to detect two faces in the image.
# Great! Our face detection system is now available as a web server. 
# However, our goal is still to make a real-time system: thanks to WebSockets, we'll be able to handle a stream of images.