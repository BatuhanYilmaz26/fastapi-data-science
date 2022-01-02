import asyncio
import pytest
from fastapi.testclient import TestClient
from Chapter09.websocket import app

# Writing tests for WebSocket endpoints
# In Chapter 8, Defining WebSockets for Two-Way Interactive Communication in FastAPI, we explained how WebSockets work and how you can implement such endpoints in FastAPI. 
# As you may have guessed, writing unit tests for WebSockets endpoints is quite different from what we've seen so far.
# Unfortunately, we won't be able to reuse HTTPX since, at the time of writing, this client can't communicate with WebSockets. 
# For the time being, our best bet is to use the default TestClient provided by Starlette.
# To show you this, we'll consider the following WebSocket example:

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def websocket_client():
    with TestClient(app) as websocket_client:
        yield websocket_client

# Then, we implemented the websocket_client fixture. 
# The TestClient class behaves as a context manager and simply expects the FastAPI application to test the argument. 
# Since we opened a context manager, we once again yielded the value to ensure the exit logic is executed after the test. 
# Notice that we don't have to manually take care of the lifespan events, contrary to what we did in the previous sections: TestClient is designed to trigger them on its own.
# Now, let's write a test for our WebSocket using this fixture:

@pytest.mark.asyncio
async def test_websocket_echo(websocket_client: TestClient):
    with websocket_client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello")

        message = websocket.receive_text()
        assert message == "Message text was: Hello"

# The first thing to notice is that we still define our test as async, with the associated asyncio marker, even if TestClient works synchronously. 
# Once again, this is useful if you need to call asynchronous services during your tests and limit the issues you may encounter with event loops.

# As you can see, the test client exposes a websocket_connect method to open a connection to a WebSocket endpoint. 
# It also works as a context manager, giving you the websocket variable. 
# It's an object that exposes several methods to either send or receive data. 
# Each of those methods will block until a message has been sent or received.

# Here, to test our "echo" server, we send a message thanks to the send_text method.
# Then, we retrieve a message with receive_text and assert that it corresponds to what we expect. 
# Equivalent methods also exist for sending and receiving JSON data directly: send_json and receive_json.

# This is what makes WebSocket testing a bit special: you have to think about the sequence of sent and received messages and implement them programmatically to test the behavior of your WebSocket.