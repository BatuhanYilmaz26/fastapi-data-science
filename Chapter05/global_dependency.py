from typing import Optional
from fastapi import FastAPI, Depends, Header, HTTPException, status

# Use a dependency on a whole application
# If you have a dependency that implements some logging or rate-limiting functionality, 
    # for example, it could be interesting to execute it for every endpoint of your API. 
# Fortunately, FastAPI allows this, as you can see in the following example:

def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status.HTTP_403_FORBIDDEN)

app = FastAPI(dependencies=[Depends(secret_header)])

@app.get("/route1")
async def route1():
    return {"route": "route1"}

@app.get("/route2")
async def route2():
    return {"route": "route2"}

# Once again, you only have to set the dependencies argument directly on the main FastAPI class. 
# Now, the dependency is applied to every endpoint in your API!