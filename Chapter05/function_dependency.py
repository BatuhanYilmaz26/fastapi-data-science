from typing import Tuple
from fastapi import FastAPI, Depends

# Creating and using a function dependency
# In FastAPI, a dependency can be defined either as a function or as a callable class. 
# In this section, we'll focus on the functions, which are the ones you'll probably work with most of the time.

# As we said, a dependency is a way to wrap some logic that will retrieve some sub-values or sub-objects, 
    # make something with them, and finally return a value that will be injected into the endpoint calling it.

# Let's look at a first example where we define a function dependency to retrieve 
    # the pagination query parameters, skip and limit:

app = FastAPI()

async def pagination(skip: int = 0, limit: int = 10) -> Tuple[int, int]:
    return (skip, limit)

@app.get("/items")
async def list_items(p: Tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

@app.get("/things")
async def list_things(p: Tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

# Type hint of a dependency return value
# You may have noticed that we had to type hint the result of our dependency in the path operation arguments, 
    # even though we already type hinted the dependency function itself. 
# Unfortunately, this is a limitation of FastAPI and its Depends function, which isn't able to forward the type of the dependency function. 
# Therefore, we have to type hint the result by hand, as we did here.

# There are two parts of this example:

# First, we have the dependency definition, with the pagination function. 
# You see that we define two arguments, skip and limit, which are integers with default values. 
# Those will be the query parameters on our endpoint. 
# We define them exactly like we would have done on a path operation function. 
# That's the beauty of this approach: FastAPI will recursively handle the arguments on the dependency and 
    # match them with the request data, such as query parameters or headers, if needed.
# We simply return those values as a tuple.

# Secondly, we have the path operation function, list_items, that uses the pagination dependency. 
# You see here that the usage is quite similar to what we have done for header or body values: 
    # we define the name of our resulting argument and we use a function result as a default value. 
# In the case of a dependency, we use the Depends function. 
# Its role is to take a function in the argument and execute it when the endpoint is called. 
# The sub-dependencies are automatically discovered and executed.
# In the endpoint, we have the pagination directly in the form of a tuple.

# Let's run this example with the following command:
# $ uvicorn function_dependency:app

# Now, we'll try to call the /items endpoint and see whether it's able to retrieve the query parameters. 
# You can try this with the following HTTPie command:
# $ http "http://localhost:8000/items?limit=5&skip=10"

# The limit and skip query parameters have correctly been retrieved thanks to our function dependency. 
# You can also try to call the endpoint without the query parameter and notice that it will return you the default values.