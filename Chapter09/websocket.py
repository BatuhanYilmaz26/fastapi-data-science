from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        await websocket.close()

# You may have recognized this "echo" example from Chapter 8, Defining WebSockets for Two-Way Interactive Communication in FastAPI. 
# To test this endpoint, we'll create a new fixture that will instantiate a test client for this application. 
# You can review its implementation in the next example: --> websocket_test.py