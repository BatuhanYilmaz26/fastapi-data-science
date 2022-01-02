from typing import Any, Dict
import httpx
from fastapi import FastAPI, Depends

# This feature is also very helpful when you need to write tests for logic involving external services, such as external APIs. 
# Instead of making real requests to those external services during your tests, which could cause issues or incur costs, you'll be able to replace them with another dependency that fakes the requests. 
# To understand this, we've built another example application with an endpoint for retrieving data from an external API:

app = FastAPI()


class ExternalAPI:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url="https://dummy.restapiexample.com/api/v1/"
        )

    async def __call__(self) -> Dict[str, Any]:
        async with self.client as client:
            response = await client.get("employees")
            return response.json()


external_api = ExternalAPI()


@app.get("/employees")
async def external_employees(employees: Dict[str, Any] = Depends(external_api)):
    return employees

# To call our external API, we've built a class dependency, as we saw in the Creating and using a parameterized dependency with a class section of Chapter 5, Dependency Injections in FastAPI. 
# We use HTTPX as an HTTP client to make a request to the external API and retrieve the data. 
# This external API is a dummy API containing fake data, very useful for experiments like this: https://dummy.restapiexample.com/.

# The /employees endpoint is simply injected with this dependency and directly returns the data provided by the external API.
# Of course, to test this endpoint, we don't want to make real requests to the external API: it may take time and could be subject to rate limiting. 
# Besides, you may want to test behavior that is not easy to reproduce in the real API, such as errors.
# Thanks to dependency_overrides, it's very easy to replace our ExternalAPI dependency class with another one that returns static data. 
# In the next example, you can see how we implemented such a test: --> app_external_api_test.py