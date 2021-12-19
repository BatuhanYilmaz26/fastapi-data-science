from typing import Tuple
from fastapi import FastAPI, Depends, Query

# Use class methods as dependencies
# Even if the __call__ method is the most straightforward way to make a class dependency, 
    # you can directly pass a method to Depends. 
# Indeed, as we said, it simply expects a callable as an argument, and a class method is a perfectly valid callable!

# This approach can be very useful if you have common parameters or logic that you need to reuse in slightly different cases. 
# For example, you could have one pre-trained machine learning model made with Scikit-learn. 
# Before applying the decision function, you may want to apply different pre-process steps depending on the input data.

# To do this, simply write your logic in a class method and pass it to the Depends function through the dot notation.

# You can see this in the following example, where we implement another style for our 
    # pagination dependency, with page and size parameters instead of skip and limit:

app = FastAPI()


class Pagination():
    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit
    
    async def skip_limit(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=0),
    ) -> Tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return (skip, capped_limit)
    
    async def page_size(
        self,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=0),
    ) -> Tuple[int, int]:
        capped_size = min(self.maximum_limit, size)
        return (page, capped_size)


# The logic of the two methods is quite similar. 
# We just look at different query parameters.
# Then, on our path operation functions, we set the /items endpoint to work with the skip/limit style, 
    # while the /things endpoint will work with the page/size style:

pagination = Pagination(maximum_limit=50)

@app.get("/items")
async def list_items(p: Tuple[int, int] = Depends(pagination.skip_limit)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

@app.get("/things")
async def list_things(p: Tuple[int, int] = Depends(pagination.page_size)):
    page, size = p
    return {"page": page, "size": size}

# As you see, we only have to pass the method we wish through the dot notation on the pagination object.

# To sum up, the class dependency approach is more advanced than the function approach but can be very useful for cases 
    # when you need to set parameters dynamically, perform heavy initialization logic, or reuse common logic on several dependencies.

# Until now, we've assumed that we care about the return value of the dependency. 
# While this will probably be the case most of the time, you may occasionally need to call a dependency to check for some conditions, 
    # but don't really need the returned value.
# FastAPI allows such use cases, and that's what we'll see in the next example (path_dependency.py).