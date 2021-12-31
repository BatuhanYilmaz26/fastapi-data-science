from typing import Optional
from fastapi import Cookie, FastAPI, WebSocket, status
from starlette.websockets import WebSocketDisconnect

# Using dependencies
# Just as with regular endpoints, you can use dependencies in WebSocket endpoints.
# However, since they are designed with HTTP in mind, this comes with a few drawbacks.

# First of all, you can't use security dependencies, as we showed in Chapter 7, Managing Authentication and Security in FastAPI. 
# Indeed, under the hood, most of them work by injecting the Request object, which only works for HTTP requests (we saw that WebSockets are injected in a WebSocket object instead). 
# Trying to inject those dependencies in a WebSocket context will result in an error. 
# Similarly, basic dependencies such as Query, Header, or Cookie have their quirks.
# Indeed, FastAPI is perfectly able to solve them in a WebSocket context. 
# However, if they are required, FastAPI will throw an error when they are missing. 
# Contrary to the HTTP validation error that is handled globally to render a proper 422 error, there is no handler for this WebSocket equivalent at the time of writing.

# Meanwhile, it's recommended to make all your WebSocket dependencies optional and handle missing values yourself.
# That's what we'll see in our next example. 
# In this one, we'll inject two dependencies, as follows:
    # • A username query parameter, which we'll use to greet the user on connection.
    # • A token cookie, which we'll compare with a static value, to keep the example simple. 
    # Of course, a proper strategy would be to have a proper user lookup, as we implemented in Chapter 7, Managing Authentication and Security in FastAPI. 
    # If this cookie is missing or doesn't have the required value, we'll close the WebSocket immediately with an error code.
# Let's see the implementation in the following sample:

API_TOKEN = "SECRET_API_TOKEN"

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str = "Anonymous",
    token: Optional[str] = Cookie(None),
):
    if token != API_TOKEN:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    await websocket.accept()
    await websocket.send_text(f"Hello, {username}!")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        await websocket.close()

# As you can see, injecting dependencies is no different from standard HTTP endpoints.
# Notice that we take care of providing a default value or making them optional, as we said before.
# Then, we can have our dummy authentication logic. 
# If it fails, we immediately close the socket with a status code. 
# WebSockets have their own set of status codes. 
# You can view a complete list of these on this MDN documentation page: https://developer.mozilla.org/fr/docs/Web/API/CloseEvent. 
# The most generic one when an error occurs is 1008.
# If it passes, we can start our classic echo server.