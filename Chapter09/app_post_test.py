import asyncio
import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import responses, status

from Chapter09.app_post import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://app.io") as test_client:
            yield test_client


@pytest.mark.asyncio
class TestCreatePerson:
    async def test_invalid(self, test_client: httpx.AsyncClient):
        payload = {"first_name": "John", "last_name": "Joe"}
        response = await test_client.post("/persons", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid(self, test_client: httpx.AsyncClient):
        payload = {"first_name": "John", "last_name": "Doe", "age": 30}
        response = await test_client.post("/persons", json=payload)

        assert response.status_code == status.HTTP_201_CREATED

        json = response.json()
        assert json == payload

# The first thing you may have noticed is that we wrapped our two tests inside a class. 
# While not required in pytest, it could help you organize your tests; for example, to regroup tests that concern a single endpoint. 
# Notice that, in this case, we only have to decorate the class with the asyncio marker; it will be automatically applied on single tests. 
# Also, ensure that you add the self argument to each test: since we are now inside a class, they become methods.

# As you can see, the HTTPX client makes it very easy to perform POST requests with a JSON payload: you just have to pass a dictionary to the json argument.
# Of course, HTTPX helps you build all kinds of HTTP requests with headers, query parameters, and so on. 
# Be sure to check its official documentation to learn more about its usage: https://www.python-httpx.org/quickstart/.