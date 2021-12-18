from fastapi import FastAPI, Body, HTTPException, status

# You are not limited to a simple string for the error message: you can return a dictionary or a list in order to get structured information about the error. 
# For example, take a look at the following code snippet:

app = FastAPI()

@app.post("/password")
async def check_password(password: str = Body(...), password_confirm: str = Body(...)):
    if password != password_confirm:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Passwords don't match.",
                "hints": [
                    "Check the caps lock on your keyboard",
                    "Try to make the password visible by clicking on the eye icon to check your typing",
                ],
            },
        )
    return {"message": "Passwords match."}

# Let's examine how it works:

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn raise_errors2:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http POST http://localhost:8000/password password="aa" password_confirm="bb"

# Here, we get a 400 status code, error message and some useful hints about the error.