from fastapi import FastAPI
from fastapi.param_functions import Query

# We also have access to more advanced validations through the Query function. 
# It works in the same way that we demonstrated in the Path parameters section:

app = FastAPI()

@app.get("/users")
async def get_user(page: int = Query(1, gt=0), size: int = Query(10, le=100)):
    return {"page": page, "size": size}

# Here, we force the page to be greater than 0 and the size to be less than or equal to 100.
# Notice how the default parameter value is the first argument of the Query function.