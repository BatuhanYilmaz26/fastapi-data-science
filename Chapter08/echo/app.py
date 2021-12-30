from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

# Creating a WebSocket with FastAPI
# Thanks to Starlette, FastAPI has built-in support to serve WebSockets. 
# As we'll see, defining a WebSocket endpoint is quick and easy, and we'll be able to get started in minutes. 
# However, things will get more complex as we try to add more features to our endpoint logic. 
# Let's start simple, with a WebSocket that waits for messages and simply echoes them back.
# In the following example, you'll see the implementation of such a simple case:

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data} ")
    except WebSocketDisconnect:
        await websocket.close()

# The code is quite understandable by itself, but let's focus on the important parts that differ from classic HTTP endpoints.

# First of all, you see that FastAPI provides a special websocket decorator to create a WebSocket endpoint. 
# As for regular endpoints, it takes as an argument the path at which it'll be available. 
# However, other arguments not making sense in this context, such as the status code or response model, are not available.
# Then, in the path operation function, we can inject a WebSocket object, which will provide us all the methods to work with the WebSocket, as we'll see.

# The first method we are calling in the implementation is accept. 
# This method should be called first as it tells the client that we agree to open the tunnel.

# After that, you see that we start an infinite loop. 
# That's the main difference with an HTTP endpoint: since we are opening a communication channel, it'll remain open until the client or the server decides to close it. 
# While it's open, they can exchange as many messages as they need, hence the infinite loop is here to keep it open and repeat the logic until the tunnel is closed.

# Inside the loop, we make a first call to the receive_text method. 
# As you may have guessed, this returns us the data sent by the client in plain text format. 
# It's important here to understand that this method will block until data is received from the client. 
# Until that event, we won't proceed with the rest of the logic.

# We see here the importance of asynchronous input/output. 
# By creating an infinite loop waiting for incoming data, we could have blocked the whole server process in a traditional blocking paradigm. 
# Here, thanks to the event loop, the process is able to answer other requests made by other clients while we are waiting for this one.

# When data is received, the method returns the text data and we can proceed with the next line. 
# Here, we simply send back the message to the client thanks to the send_text method.
# Once done, we are going back to the beginning of the loop to wait for another message.

# You probably noticed that the whole loop is wrapped inside a try..except statement.
# This is necessary to handle client disconnection. 
# Indeed, our server will most of the time be blocked at the receive_text line, waiting for client data. 
# If the client decides to disconnect, the tunnel will be closed and the receive_text call will fail, with a WebSocketDisconnect exception. 
# That's why it's important to catch it to break the loop and properly call disconnect on the server side.

# Let's try it! You can run the FastAPI application, as usual, thanks to the Uvicorn server.
# Here's the command you'll need:
# $ uvicorn Chapter08.echo.app:app

# Our client will be a simple HyperText Markup Language (HTML) page with some JavaScript code to interact with the WebSocket. 
# We'll quickly go through this code after the demonstration. 
# To run it, we can simply serve it with the built-in Python server, as follows:
# $ python -m http.server --directory Chapter08/echo 9000
# This will serve our HTML page on port 9000 of your local machine. 
# If you open the http://localhost:9000 address, you'll see a simple interface.