import numpy as np
import asyncio
import cv2
from typing import List, Tuple
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, websockets
from pydantic import BaseModel

# Implementing a WebSocket to perform face detection on a stream of images
# One of the main benefits of WebSockets, is that it opens a full-duplex communication channel between the client and the server.
# Once the connection is established, messages can be passed quickly without having to go through all the steps of the HTTP protocol. 
# Therefore, it's much more suited to sending lots of messages in real time.

# The point here will be to implement a WebSocket endpoint that is able to both accept image data and run OpenCV detection on it. 
# The main challenge here will be to handle a phenomenon known as backpressure. 
# Put simply, we'll receive more images from the browser than the server is able to handle, because of the time needed to run the detection algorithm. 
# Thus, we'll have to work with a queue (or buffer) of limited size and drop some images along the way to handle the stream in near real time.
# You can read the implementation in the following sample:


app = FastAPI()
cascade_classifier = cv2.CascadeClassifier()


class Faces(BaseModel):
    faces: List[Tuple[int, int, int, int]]


async def receive(websocket: WebSocket, queue: asyncio.Queue):
    bytes = await websocket.receive_bytes()
    try:
        queue.put_nowait(bytes)
    except asyncio.QueueFull:
        pass


async def detect(websocket: WebSocket, queue: asyncio.Queue):
    while True:
        bytes = await queue.get()
        data = np.frombuffer(bytes, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = cascade_classifier.detectMultiScale(gray)
        if len(faces) > 0:
            faces_output = Faces(faces=faces.tolist())
        else:
            faces_output = Faces(faces=[])
        await websocket.send_json(faces_output.dict())


@app.websocket("/face-detection")
async def face_detection(websocket: WebSocket):
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue(maxsize=10)
    detect_task = asyncio.create_task(detect(websocket, queue))
    try:
        while True:
            await receive(websocket, queue)
    except WebSocketDisconnect:
        detect_task.cancel()
        await websocket.close()


@app.on_event("startup")
async def startup():
    cascade_classifier.load(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )


# As we said, we have two tasks: receive and detect. 
# The first one is for reading raw bytes from the WebSocket, while the second one is for performing the detection and sending the result.

# The key here is to use the asyncio.Queue object. 
# This is a convenient structure allowing us to queue some data in memory and retrieve it in a first in, first out (FIFO) strategy. 
# We are able to set a limit on the number of elements we store in the queue: this is how we'll be able to limit the number of images we handle.

# The receive function is receiving data and putting it at the end of the queue. 
# When working with Queue, we have two methods to put a new element in the queue: put and put_nowait.
# If the queue is full, the first one will wait until there is room in the queue.
# This is not what we want here: we want to drop images that we won't be able to handle in time. 
# With put_nowait, the QueueFull exception is raised if the queue is full. 
# In this case, we just pass and drop the data.

# On the other hand, the detect function is pulling the first message from the queue and runs its detection before sending the result. 
# In the previous example (api.py), we used the fromfile function to read the image data. 
# Here, we directly have bytes data, so frombuffer is more appropriate.

# The implementation of the WebSocket itself is a bit different from what we saw in Chapter 8.
# Indeed, we don't want the two tasks to be concurrent here: we want to accept new images and continuously run detections on images as they come in.
# This is why the detect function has its own infinite loop. By using create_task on this function, we schedule it in the event loop so that it starts to handle the images in the queue.
# Then, we have the regular WebSocket loop, which calls the receive function. 
# In a sense, we could say that that detect runs "in the background." 
# Notice that we ensure that this task is canceled when the WebSocket is closed so that the infinite loop is correctly stopped.

# Our backend is now ready! Let's now see how to use its power from a browser.

# • In one terminal, launch the FastAPI application:
# $ Chapter14.websocket_face_detection.app:app

# • In another terminal, serve the HTML application with the built-in Python server:
# $ python -m http.server --directory chapter14/websocket_face_detection 9000

# The HTML application is now ready on port 9000. 
# You can access it in your browser with the address http://localhost:9000. 
# You'll see an interface inviting you to choose the camera you want to use.
# Select the webcam you wish to use and click on Start. 
# The video output will show up, face detection will start via the WebSocket and green rectangles will be drawn around the detected faces.