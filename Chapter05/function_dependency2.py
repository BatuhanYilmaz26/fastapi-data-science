from typing import Tuple
from fastapi import FastAPI, Depends, Query

# In addition to the previous example (function_dependency.py), 
# we can do more complex things in those dependencies, just like we would in a regular path operation function. 
# In the following example, we add some validation to those pagination parameters and cap the limit at 100:

app = FastAPI()

async def pagination(
    skip: int = Query(0, ge=0), # 0 -> default value, ge=0 -> greater than or equal to 0
    limit: int = Query(10, ge=0), # 10 -> default value, ge=0 -> greater than or equal to 0
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)

@app.get("/items")
async def list_items(p: Tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

@app.get("/things")
async def list_things(p: Tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

# As you can see, our dependency starts to become more complex:
# • We added the Query function to our arguments to add a validation constraint:
    # now, an error 422 will be raised if skip or limit are negative integers.
# • We ensure that the limit is, at most, 100.

# The code on our path operation functions doesn't have to change: we have a clear separation of concern between the logic of the 
    # endpoint and the more generic logic for the pagination parameters.