from fastapi import FastAPI

# Query parameters are a common way to add some dynamic parameters to a URL. 
# You find them at the end of the URL in the following form: ?param1=foo&param2=bar. 
# In a REST API, they are commonly used on read endpoints to apply pagination, a filter, a sorting order, or selecting fields.
# They use the exact same syntax as path parameters:

app = FastAPI()

@app.get("/users")
async def get_user(page: int=1, size: int=10):
    return {"page": page, "size": size}

# Here, you can see that we have defined a default value for those arguments, which means they are optional when calling the API. 
# Of course, if you wish to define a required query parameter, simply leave out the default value.

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn query_parameters:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# http "http://localhost:8000/users?page=2&size=20"