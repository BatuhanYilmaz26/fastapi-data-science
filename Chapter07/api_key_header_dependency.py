from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader

# In addition to the previous example(api_key_header.py)
# We can also wrap the logic that checks the token value in its own dependency to reuse it across your endpoints, as shown in the following example:

API_TOKEN = "SECRET_API_TOKEN"

app = FastAPI()


async def api_token(token: str = Depends(APIKeyHeader(name="Token"))):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@app.get("/protected-route", dependencies=[Depends(api_token)])
async def protected_route():
    return {"hello": "world"}

# Remember that these kinds of dependencies are very good candidates to be used as router or global dependencies to protect whole sets of routes, 
    # as we saw in Chapter 5, Dependency Injections in FastAPI.
# This is a very basic example of adding authorization to your API. 
# In this example, we don't have any user management; we are only checking that a token corresponds to a constant value. 
# While it could be useful for private microservices that are not intended to be called by end users, don't consider this approach as a very secure one. 
# First, make sure your API is always served using HTTPS to ensure your token is not exposed in the headers.
# Then, if it's a private microservice, you should also consider not exposing it publicly on the internet and making sure only trusted servers can call it. 
# Since you don't need users to make requests to this service, it's much safer than a simple token key that could be stolen.

# Of course, most of the time, you'll want to authenticate real users with their own individual access token so that they can access their own data. 
# You have probably already used a service that implements this very typical pattern:
# • First, you must register an account on this service, usually by providing your email address and a password.
# • Next, you can log into the service using the same email address and password. 
# The service checks if the email address exists and that the password is valid.
# • In exchange, the service provides you with a session token that can be used on subsequent requests to authenticate yourself. 
# This way, you don't have to provide your email address and password on each request, which would be annoying and dangerous.
# Usually, such session tokens have a limited lifetime, which means you'll have to log in again after some time. 
# This mitigates any security risks if the session token is stolen.