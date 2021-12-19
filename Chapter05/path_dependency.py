from typing import Optional
from fastapi import FastAPI, Depends, Header, HTTPException, status

# Using dependencies at a path, router, and global level 
# As we said, dependencies are the recommended way to create building blocks in a FastAPI project, allowing you to reuse logic across endpoints while maintaining maximum code readability. 
# Until now, we've applied them on a single endpoint, but couldn't we expand this approach to a whole router? 
    # Or even a whole FastAPI application? Actually, we can!

# The main motivation for this is to be able to apply some global request validation or 
    # perform side logic on several routes without the need to add the dependency on each endpoint. 
# Typically, an authentication method or a rate-limiter could be very good candidates for this use case.

# To show you how it works, we'll implement a simple dependency that we will use across all the following examples. 
# You can see it in the following example:

app = FastAPI()

def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status.HTTP_403_FORBIDDEN)

# This dependency will simply look for a header in the request named Secret-Header.
# If it's missing or not equal to SECRET_VALUE, it will raise a 403 error. 
# Please note that this approach is only for the sake of the example; there are better ways to secure your API, 
    # which we'll cover in Chapter 7, Managing Authentication and Security in FastAPI.

# Use a dependency on a path decorator
# Until now, we've assumed that we were always interested in the return value of the dependency. 
# As our secret_header dependency clearly shows here, this is not always the case. 
# This is why you can add a dependency on a path operation decorator instead of the arguments. 
# You can see how in the following example:

@app.get("/protected_route", dependencies=[Depends(secret_header)])
async def protected_route():
    return {"hello": "world"}

# The path operation decorator accepts an argument, dependencies, which expects a list of dependencies. 
# You see that, just like for dependencies you pass in arguments, you need to wrap your function (or callable) with the Depends function.

# Now, whenever the /protected-route route is called, the dependency will be called and will check for the required header. 
# As you may have guessed, since dependencies is a list, you can add as many dependencies as you need.

# That's interesting, but what if we want to protect a whole set of endpoints? 
# It would be a bit cumbersome and error-prone to add it manually on each one. 
# Fortunately, FastAPI provides a way to do that. 
    # We will see that in the next example --> router_dependency.py