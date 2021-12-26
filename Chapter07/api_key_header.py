from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader

# Security dependencies in FastAPI
# To protect a REST API and, more generally, HTTP endpoints, lots of standards have been proposed. 
# Here is a non-exhaustive list of the most common ones:

# • Basic HTTP authentication: In this scheme, user credentials (usually, an identifier such as an email address and password) are put into an HTTP header called Authorization. 
# The value consists of the Basic keyword, followed by the user credentials encoded in Base64. 
# This is a very simple scheme to implement but not very secure since the password appears in every request.
# • Cookies: Cookies are a useful way to store static data on the client side, usually on web browsers, that is sent in each request to the server. 
# Typically, a cookie can contain a session token that can be verified by the server and linked to a specific user.
# • Tokens in the Authorization header: Probably the most used header in a REST API context, this simply consists of sending a token in an HTTP Authorization header. 
# The token is often prefixed by a method keyword, such as Bearer. 
# On the server side, this token can be verified and linked to a specific user.

# Each standard has its pros and cons and is suitable for a specific use case.
# As we already know, FastAPI is mainly about dependency injection and callables that are automatically detected and called at runtime. 
# Authentication methods are no exception: FastAPI provides most of them out of the box as security dependencies.

# First, let's learn how to retrieve an access token in an arbitrary header. 
# For this, we can use the ApiKeyHeader dependency, as shown in the following example:

API_TOKEN = "SECRET_API_TOKEN"

app = FastAPI()
api_key_header = APIKeyHeader(name="Token")


@app.get("/protected-route")
async def protected_route(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"hello": "world"}

# In this simple example, we hardcoded a token, API_TOKEN, and checked if the one that was passed in the header is equal to this token, 
    # before authorizing the endpoint to be called. 
# To do this, we used the APIKeyHeader security dependency, which is designed to retrieve a value from a header. 
# It's a class dependency that can be instantiated with arguments. 
# It also accepts the name argument, which will be the name of the header it'll look for.

# Then, in our endpoint, we injected this dependency to get the token's value. 
# If it's equal to our token constant, we proceed with the endpoint logic. 
# Otherwise, we raise a 403 error.