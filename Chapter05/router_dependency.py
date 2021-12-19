from typing import Optional
from fastapi import APIRouter, FastAPI, Depends, Header, HTTPException, status

# Use a dependency on a whole router
# If you recall the Structure a bigger project with multiple routers section in Chapter 3, Developing a RESTful API with FastAPI, 
    # you know that you can create several routers in your project to clearly split the different parts of your API 
    # and "wire" them to your main FastAPI application. 
# This is done with the APIRouter class and the include_router method of the FastAPI class.

# With this approach, it can be interesting to inject a dependency on the whole router, so that it's called for every route of this router. 
# You have two ways of doing this:
# First way:
# • Set the dependencies argument on the APIRouter class, as you can see in the following example:

def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status.HTTP_403_FORBIDDEN)

router = APIRouter(dependencies=[Depends(secret_header)])

@router.get("/route1")
async def router_route1():
    return {"route": "route1"}

@router.get("/router2")
async def router_route2():
    return {"route": "route2"}

app = FastAPI()
app.include_router(router, prefix="/router")