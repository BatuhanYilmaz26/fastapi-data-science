import asyncio
from typing import List

import httpx
from py import test
import pytest
from asgi_lifespan import LifespanManager
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import status

from Chapter06.mongodb.app import app, get_database
from Chapter06.mongodb.models import PostDB

# Testing with a database
# Your application will likely have a database connection to read and store data. 
# In this context, you'll need to work with a fresh test database at each run to have a clean and predictable set of data to write your tests.
# For this, we'll use two things. 
# The first one, dependency_overrides, is a FastAPI feature that allows us to replace some dependencies at runtime. 
# For example, we can replace the dependency that returns the database instance with another one that returns a test database instance. 
# The second one is, once again, fixtures, which will help us create fake data in the test database before we run the tests.

# For our tests, we'll create a new instance of AsyncIOMotorDatabase that points to another database. 
# Then, we'll create a new dependency, directly in our test file, that returns this instance. 
# You can see this in the following example:

motor_client = AsyncIOMotorClient("mongodb://localhost:27017")
database_test = motor_client["Chapter09_db_test"]


def get_test_database():
    return database_test


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

# Then, in our test_client fixture, we'll override the default get_database dependency by using our current get_test_database dependency. 
# The following example shows how this is done:

@pytest.fixture
async def test_client():
    app.dependency_overrides[get_database] = get_test_database
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://app.io") as test_client:
            yield test_client

# FastAPI provides a property called dependency_overrides, which is a dictionary that maps original dependency functions with substitutes. 
# Here, we directly used the get_database function as a key. The rest of the fixture doesn't have to change. 
# Now, whenever the get_database dependency is injected into the application code, FastAPI will automatically replace it with get_test_database. 
# As a result, our endpoints will now work with the test database instance.

# To test some behaviors, such as retrieving a single post, it's usually convenient to have some base data in our test database. 
# To allow this, we'll create a new fixture that will instantiate dummy PostDB objects and insert them into the test database. 
# You can see this in the following example:

@pytest.fixture(autouse=True, scope="module")
async def initial_posts():
    initial_posts[
        PostDB(title="Post 1", content="Content 1"),
        PostDB(title="Post 2", content="Content 2"),
        PostDB(title="Post 3", content="Content 3"),
    ]
    await database_test["posts"].insert_many(
        [post.dict(by_alias=True) for post in initial_posts]
    )

    yield initial_posts

    await motor_client.drop_database("Chapter09_db_test")

# Here, you can see that we just had to make an insert_many request to the MongoDB database to create the posts.
# Notice that we used the autouse and scope arguments of the fixture decorator. 
# The first one tells pytest to automatically call this fixture even if it's not requested in any test.
# In this case, it's convenient because we'll always ensure that the data has been created in the database, without the risk of forgetting to request it in the tests. 
# The other one, scope, allows us, as we mentioned previously, to not run this fixture at the beginning of each test.
# With the module value, the fixture will create the objects only once, at the beginning of this particular test file. 
# It helps us keep the test fast because in this case, it doesn't make sense to recreate the posts before each test.

# Once again, we yield the posts instead of returning them. 
# This pattern allows us to delete the test database after the tests run. 
# By doing this, we're making sure that we always start with a fresh database when we've run the tests.
# And we are done! We can now write tests while knowing exactly what we have in the database. 

# In the following example, you can see tests that are used to verify the behavior of the endpoint retrieving a single post:

@pytest.mark.asyncio
class TestGetPost:
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/posts/abc")

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    async def test_existing(
        self, test_client: httpx.AsyncClient, initial_posts: List[PostDB]
    ):
        response = await test_client.get(f"/posts/{initial_posts[0].id}")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json["_id"] == str(initial_posts[0].id)

# Notice that we requested the initial_posts fixture in the second test to retrieve the identifier of the truly existing post in our database.

# Of course, we can also test our endpoints by creating data and checking if they correctly insert this data into the database. 
# You can see this in the following example:

@pytest.mark.asyncio
class TestCreatePost:
    async def test_invalid_payload(self, test_client: httpx.AsyncClient):
        payload = {"title": "New post"}
        response = await test_client.post("/posts", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_payload(self, test_client: httpx.AsyncClient):
        payload = {"title": "New post", "content": "New post content"}
        response = await test_client.post("/posts", json=payload)

        assert response.status_code == status.HTTP_201_CREATED

        json = response.json()
        post_id = ObjectId(json["_id"])
        post_db = await database_test["posts"].find_one({"_id": post_id})
        assert post_db is not None

# In the second test, we used the database_test instance to perform a request and check that the object was inserted correctly. 
# This shows the benefit of using asynchronous tests: we can use the same libraries and tools inside our tests.