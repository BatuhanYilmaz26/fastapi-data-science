import asyncio
import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import status

from Chapter09.app import app

# The first one, event_loop, will ensure that we always work with the same event loop instance. 
# It's automatically requested by pytest-asyncio before executing asynchronous tests. 
# While not strictly required, experience has shown us that it greatly helps us avoid errors that may occur when several event loops are launched. 
# You can see its implementation in the following example: 

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

# Here, you can see that we simply get the current event loop before yielding it. 
# Using a generator allows us to "pause" the function's execution and get back to the execution of its caller. 
# This way, when the caller is done, we can execute cleanup operations, such as closing the loop. 
# pytest is smart enough to handle this correctly in fixtures, so this is a very common pattern for setting up test data, using it, and destroying it after.

# Of course, this function is decorated with the fixture decorator to make it a fixture for pytest. 
# You may have noticed that we added an argument called scope with a value of session. 
# This argument controls at which level the fixture should be instantiated.
# By default, it's recreated at the beginning of each single test function. 
# The session value is the highest level, meaning that the fixture is only created once at the beginning of the whole test run, which is relevant for our event loop. 
# You can find out more about this more advanced feature in the official documentation: https://docs.pytest.org/en/latest/how-to/fixtures.html#scope-sharing-fixtures-acrossclasses-modules-packages-or-session.

# Next, we'll implement our test_client fixture, which will create an instance of HTTPX for our FastAPI application. 
# We must also remember to trigger the app events with asgi-lifespan. 
# You can see what it looks like in the following example:

@pytest.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://app.io") as test_client:
            yield test_client

# Only three lines are needed. 
# Notice that the app variable is our FastAPI application instance is the one we imported from its module, from Chapter09.app import app

# Up until now, we haven't had the opportunity to talk about the with syntax. 
# In Python, this is what's called a context manager. 
# Simply put, it's a convenient syntax for objects that need to execute setup logic when they are used and teardown logic when they are not needed anymore. 
# When you enter the with block, the object automatically executes the setup logic. 
# When you exit the block, it executes its teardown logic. 
# You can read more about context managers in the Python documentation: https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers.

# In our case, both LifespanManager and httpx.AsyncClient work as context managers, so we simply have to nest their blocks. 
# The first one ensures startup and shutdown events are executed, while the second one ensures that an HTTP session is ready.

# Notice that we once again used a generator here, with yield. 
# This is important because, even if we don't have any more code after, we have to give the context managers the opportunity to exit: after the yield statement, we implicitly exit the with blocks.


# Writing tests for REST API endpoints
# All the tools we need to test our FastAPI application are now ready. 
# All these tests boil down to performing an HTTP request and checking the response to see if it corresponds to what we expect.
# Let's start simple with a test for our hello_world path operation function. 
# You can see it in the following code:

@pytest.mark.asyncio
async def test_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/")

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json == {"hello": "world"}

# First of all, notice that the test function is defined as async. 
# As we mentioned previously, to make it work with pytest, we had to install pytest-asyncio. 
# This extension provides the asyncio marker: each asynchronous test should be decorated with this marker to make it work properly.

# Next, we requested our test_client fixture, which we defined earlier. 
# It gives us an HTTPX client instance ready to make requests to our FastAPI app. 
# Note that we manually type hinted the fixture. 
# While not strictly required, it'll greatly help you if you use an IDE such as Visual Studio Code, which uses type hints to provide you with convenient autocompletion features.

# Then, in the body of our test, we performed the request. 
# Here, it's a simple GET request to the / path. 
# It returns an HTTPX Response object (which is different from the Response class of FastAPI) containing all the data of the HTTP response: the status code, the headers, and the body.

# Finally, we made assertions based on this data. As you can see, we verified that the status code was indeed 200. 
# We also checked the content of the body, which is a simple JSON object. 
# Notice that the Response object has a convenient method called json for automatically parsing JSON content.