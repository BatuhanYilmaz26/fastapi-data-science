from fastapi import FastAPI, Path

# Advanced Validation
# In this example, we'll only allow an id argument that is greater than or equal to 1:
app = FastAPI()

@app.get("/users/{id}")
async def get_user(id: int = Path(..., ge=1)): 
    # The result of Path is used as a default value for the id argument in the path 
        # operation function.
    # Ellipses are here to tell FastAPI that we don't want a default value.
    # Then, we can add the keyword arguments that we are interested in.
        # In our example, this is ge.
        # ge: Greater than or equal to
    return {"id": id}