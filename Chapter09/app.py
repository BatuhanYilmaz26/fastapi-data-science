from fastapi import FastAPI

# Setting up testing tools for FastAPI with HTTPX
# If you look at the FastAPI documentation regarding testing, you'll see that it recommends that you use TestClient provided by Starlette. 
# In this book, we'll show you a different approach involving an HTTP client, called HTTPX.

# Why? The default TestClient is implemented in a way that makes it completely synchronous, meaning you can write tests without worrying about async and await.
# This might sound nice, but we found that it causes some problems in practice: since your FastAPI app is designed to work asynchronously, 
    # you'll likely have lots of services working asynchronously, such as the database drivers we saw in Chapter 6, Databases and Asynchronous ORMs. 
# Thus, in your tests, you'll probably need to perform some actions on those asynchronous services, such as filling a database with dummy data, 
    # which will make your tests asynchronous anyway. 
# Melting the two approaches often leads to strange errors that are hard to debug.

# Fortunately, HTTPX, an HTTP client created by the same team as Starlette, allows us to have a pure asynchronous HTTP client able to make requests to our FastAPI app. 
# To make this approach work, we'll need three libraries:
# • HTTPX, the client that will perform HTTP requests 
# • asgi-lifepsan, a library for managing the startup and shutdown events of your FastAPI app programmatically
# • pytest-asyncio, an extension of pytest that allows us to write asynchronous tests

# Now, let's write some fixtures so that we can easily get an HTTP test client for a FastAPI application. 
# This way, when writing a test, we'll only have to request the fixture and we'll be able to make a request right away.
# In the following example, we are considering a simple FastAPI application that we want to test:

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"hello": "world"}


@app.on_event("startup")
async def startup():
    print("Startup")


@app.on_event("shutdown")
async def shutdown():
    print("Shutdown")

# In a separate test file, we'll implement two fixtures. --> app_test.py