from typing import Tuple
from fastapi import FastAPI, Depends, Query
from fastapi.param_functions import Path

# Creating and using a parameterized dependency with a class
# In the previous section, we defined dependencies as regular functions, which works well in most cases. 
# Still, you may need to set some parameters on a dependency to finely tune its behavior. 
# Since the arguments of the function are set by the dependency injection system, we can't add an argument to the function.

# In the pagination example, we added some logic to cap the limit value at 100.
# If we wanted to set this maximum limit dynamically, how would we do that?

# The solution is to create a class that will be used as a dependency. 
# This way, we can set class properties, with the __init__ method, for example, and use them in the logic of the dependency itself. 
# This logic will be defined in the __call__ method of the class. 
# If you remember what we learned in the Callable object section of Chapter 2, Python Programming Specificities, 
    # you know that it makes the object callable, meaning it can be called like a regular function. 
# Actually, that is all that Depends requires for a dependency: being a callable. 
# We'll use this property to create a parameterized dependency thanks to a class.

# In the following example, we reimplemented the pagination example with a class, 
    # allowing us to set the maximum limit dynamically:

app = FastAPI()


class Pagination:
    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit
    
    async def __call_(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=0),
    ) -> Tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return (skip, capped_limit)


# As you can see, the logic in the __call__ method is the same as in the function we defined in the previous example. 
# The only difference here is that we can pull our maximum limit from our class properties 
    # that we can set at the object initialization.

# Then, you can simply create an instance of this class and use it as a dependency with Depends 
    # on your path operation function, as you can see in the following code block:

pagination = Pagination(maximum_limit=50)

@app.get("/items")
async def list_items(p: Tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

@app.get("/things")
async def list_things(p: Tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

# Here, we hardcoded the value 50, but we could very well pull it from a configuration file or an environment variable.

# The other advantage of a class dependency is that it can maintain local values in memory.
# This property can be very useful if we have to make some heavy initialization logic, 
    # such as loading a machine learning model, for example, that we want to do only once at startup.
# Then, the callable part just has to call the loaded model to make the prediction, which should be quite fast.