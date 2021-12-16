from fastapi import FastAPI, Path

# In the following example, we want to define a path parameter that 
    # accepts license plates in the form of AB-123-CD (French license plates). 
# The first approach would be to force the string to be of length 9 
    # (that is, two letters, a dash, three digits, a dash, and two letters):

app = FastAPI()

@app.get("/license-plates/{license}")
async def get_license_plate(license: str = Path(..., min_length=9, 
max_length=9)):
    return {"license": license}