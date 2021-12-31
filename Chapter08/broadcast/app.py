import asyncio

from broadcaster import Broadcast
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect

# In the following example, you'll see the instantiation of the Broadcaster object:

app = FastAPI()
broadcast = Broadcast("redis://localhost:6379")
CHANNEL = "CHAT"

# As you can see, it only expects a URL to our Redis server. 
# Notice also that we define a CHANNEL constant. 
# This will be the name of the channel to publish and subscribe to messages. 
# We choose a static value here for the sake of the example, but you could have dynamic channel names in a real-world application—to support several chat rooms, for example.

# Then, we define two functions: one to subscribe to new messages and send them to the client and another one to publish messages received in the WebSocket. 
# You can see these functions in the following sample:

class MessageEvent(BaseModel):
    username: str
    message: str


async def receive_message(websocket: WebSocket, username: str):
    async with broadcast.subscribe(channel=CHANNEL) as subscriber:
        async for event in subscriber:
            message_event = MessageEvent.parse_raw(event.message)
            # Discard user's own messages
            if message_event.username != username:
                await websocket.send_json(message_event.dict())


async def send_message(websocket: WebSocket, username: str):
    data = await websocket.receive_text()
    event = MessageEvent(username=username, message=data)
    await broadcast.publish(channel=CHANNEL, message=event.json())

# First of all, notice that we defined a Pydantic model, MessageEvent, to help us structure the data contained in a message. 
# Instead of just passing raw strings as we've been doing up to now, we have an object bearing both the message and the username.

# The first function, receive_message, subscribes to the broadcast channel and waits for messages called event. 
# The data of the message contains serialized JavaScript Object Notation (JSON) that we deserialize to instantiate a MessageEvent object. 
# Notice that we use the parse_raw method of the Pydantic model, allowing us to parse the JSON string into an object in one operation.
# Then, we check if the message username is different from the current username. 
# Indeed, since all users are subscribed to the channel, they will also receive the messages they sent themselves. 
# That's why we discard them based on the username to avoid this. 
# Of course, in a real-world application, you'll likely want to rely on a unique user identifier (UID) rather than a simple username.
# Finally, we can send the message through the WebSocket thanks to the send_json method, which takes care of serializing the dictionary automatically.

# The second function, send_message, is there to publish a message to the broker. 
# Quite simply, it waits for new data in the socket, structures it into a MessageEvent object, and then publishes it.

# That's about it for the broadcaster part. 
# We then have the WebSocket implementation in itself, which is very similar to what we saw in the previous sections. 
# You can see it in the following sample:

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str = "Anonymous"):
    await websocket.accept()
    try:
        while True:
            receive_message_task = asyncio.create_task(receive_message(websocket, username))
            send_message_task = asyncio.create_task(send_message(websocket, username))
            done, pending = await asyncio.wait(
                {receive_message_task, send_message_task},
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            for task in done:
                task.result()
    except WebSocketDisconnect:
        await websocket.close()

# Notice that username is retrieved from the query parameters.

# Finally, we need to tell FastAPI to open the connection with the broker when it starts the application and to close it when exiting, 
    # as you can see in the following extract:

@app.on_event("startup")
async def startup():
    await broadcast.connect()


@app.on_event("shutdown")
async def shutdown():
    await broadcast.disconnect()

# The on_event decorators allow us to trigger some useful logic when FastAPI starts or stops.

# Let's now try this application! 
# First, we'll run the Uvicorn server. 
# Be sure that your Redis container is running before starting.
# Here's the code you'll need:
# $ uvicorn Chapter08.broadcast.app:app

# We also provided a simple HTML client in the examples. 
# To run it, we can simply serve it with the built-in Python server, as follows:
# $ python -m http.server --directory Chapter08/broadcast 9000

# You can now access it through http://localhost:9000. 
# If you open it twice in your browser, in two different windows, you can see whether the broadcasting is working. 
# Input a username in the first window and click on Connect. 
# Do the same in the second window with a different username. 
# You can now send messages and see that they are broadcasted to the other client.