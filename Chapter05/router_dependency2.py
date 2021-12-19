from typing import Optional
from fastapi import APIRouter, FastAPI, Depends, Header, HTTPException, status

# Second way:
# • Set the dependencies argument on the include_router method, as you can see in the following example:

def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status.HTTP_403_FORBIDDEN)

router = APIRouter()

@router.get("/route1")
async def router_route1():
    return {"route": "route1"}

@router.get("/route2")
async def router_route2():
    return {"route": "route2"}

app = FastAPI()
app.include_router(router, prefix="/router", dependencies=[Depends(secret_header)])

# In both cases, the dependencies argument expects a list of dependencies. 
# You see that, just like for dependencies you pass in arguments, you need to wrap your function (or callable) with the Depends function. 
# Of course, since it's a list, you can add several dependencies if you need.

# Now, how to choose between the two approaches? 
# In both cases, the effect will be exactly the same, so we could say it doesn't really matter. 
# Philosophically, we could say that we should declare a dependency on the APIRouter class if it's needed in the context of this router.
# Put another way, we could ask ourselves the question, Does this router work without this dependency if we run it independently? 
    # If the answer to this question is no, then you should probably set the dependency on the APIRouter class. 
    # Otherwise, declaring it in the include_router method may make more sense. 
# But again, this is an intellectual choice that won't change the functionality of your API, 
    # so feel free to choose the one you're more comfortable with.

# We are now able to set dependencies for a whole router. 
# In some cases, it could also be interesting to declare them for a whole application! 
    # We will see that in the next example --> global_dependency.py