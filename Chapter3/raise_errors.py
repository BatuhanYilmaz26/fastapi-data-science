from fastapi import FastAPI, Body, HTTPException, status

# To raise an HTTP error in FastAPI, you'll have to raise a Python exception, HTTPException. 
# This exception class will allow us to set a status code and an error message. 
# It is caught by FastAPI error handlers that take care of forming a proper HTTP response.

# In the following example, we'll raise a 400 Bad Request error if the password and password_confirm payload properties don't match:

app = FastAPI()

@app.post("/password")
async def check_password(password: str = Body(...), password_confirm: str = Body(...)):
    if password != password_confirm:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Passwords don't match.",
        )
    return {"message": "Passwords match."}

# As you can see here, if the passwords are not equal, we directly raise HTTPException.
# The first argument is the status code, and the detail keyword argument lets us write an error message.
# Let's examine how it works:

# To run this API: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn raise_errors:app

# Next step is to try our endpoint with HTTPie: 
    # (start a new terminal besides the one running the uvicorn command)
# $ http POST http://localhost:8000/password password="aa" password_confirm="bb"

# Here, we do get a 400 status code and our error message has been wrapped nicely in a JSON object with the detail key. 
# This is how FastAPI handles errors by default.