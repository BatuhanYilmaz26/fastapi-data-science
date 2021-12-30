import asyncio
from datetime import datetime

from fastapi import FastAPI, WebSocket, status
from starlette.websockets import WebSocketDisconnect

# Handling concurrency
# In the previous example, we've assumed that the client was always sending a message first: we wait for its message before sending it back. 
# Once again, it's the client that takes the initiative in the conversation.
# However, in usual scenarios, the server can have data to send to the client without being at the initiative. 
# In a chat application, another user can typically send one or several messages that we want to forward to the first user immediately. 
# In this context, the blocking call to receive_text we showed in the previous example is a problem: while we are waiting, the server could have messages to forward to the client.

# To solve this, we'll rely on more advanced tools of the asyncio module. 
# Indeed, it provides functions that allow us to schedule several coroutines concurrently and wait until one of them is complete. 
# In our context, we can have a coroutine that waits for client messages and another one that sends data to it when it arrives. 
# The first one being fulfilled wins and we can start again with another loop iteration.

# To make this clearer, let's build another example, in which the server will once again echo back the message of the client. 
# Besides that, it'll regularly send the current time to the client. 
# You can see the implementation in the following code snippet:

app = FastAPI()


async def echo_message(websocket: WebSocket):
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")


async def send_time(websocket: WebSocket):
    await asyncio.sleep(10)
    await websocket.send_text(f"It is: {datetime.utcnow().isoformat()} ")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            echo_message_task = asyncio.create_task(echo_message(websocket))
            send_time_task = asyncio.create_task(send_time(websocket))
            done, pending = await asyncio.wait(
                {echo_message_task, send_time_task},
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            for task in done:
                task.result()
    except WebSocketDisconnect:
        await websocket.close()


# As you can see, we defined two coroutines: the first one, echo_message, waits for text messages from the client and sends them back, 
    # while the second one, send_time, waits for 10 seconds before sending the current time to the client. 
# Both of them expect a WebSocket instance in the argument.

# The most interesting part lives under the infinite loop: as you can see, we call our two functions, wrapped by the create_task function of asyncio. 
# This transforms the coroutine into a Task object. 
# Under the hood, a task is how the event loop manages the execution of the coroutine. 
# Put more simply, it gives us full control over the execution of the coroutine, to retrieve its result or even cancel it.

# Those task objects are necessary to work with asyncio.wait. 
# This function is especially useful to run tasks concurrently. 
# It expects in the first argument a set of tasks to run. 
# By default, this function will block until all given tasks are completed. 
# However, we can control that thanks to the return_when argument: in our case, we want it to block until one of the tasks is completed, which corresponds to the FIRST_COMPLETED value.
# The effect is the following: our server will launch the coroutines concurrently. 
# The first one will block waiting for a client message, while the other one will block for 10 seconds.
# If the client sends a message before 10 seconds, it'll send the message back and complete.
# Otherwise, the send_time coroutine will send the current time and complete.

# At that point, asyncio.wait will return us two sets: 
    # the first one, done, contains a set of completed tasks, 
    # while the other one, pending, contains a set of tasks not yet completed.

# We want to now go back to the start of the loop to start again. 
# However, we need to first cancel all the tasks that have not been completed; 
    # otherwise, they would pile up at each iteration, hence the iteration over the pending set to cancel those tasks.

# Finally, we also make an iteration over the done tasks and call the result method on them. 
# This method returns the result of the coroutine but also re-raises an exception that could have been raised inside. 
# This is especially useful to handle once again the disconnection of the client: when waiting for client data, if the tunnel is closed, an exception is raised. 
# Thus, our try..except statement can catch it to properly close the WebSocket.