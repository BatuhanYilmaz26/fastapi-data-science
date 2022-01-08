import time
from fastapi import FastAPI

# Choosing between standard or async functions
# You may have noticed that we changed the predict method and the prediction and delete_cache path operation functions so that they're standard, non-async functions.
# Since the beginning of this book, we've shown you how FastAPI completely embraces asynchronous I/O and why it's good for the performance of your applications. 
# We've also recommended libraries that also work asynchronously, such as database drivers, to leverage that power.

# In some cases, however, that's not always possible. 
# In this case, Joblib is implemented to work synchronously. 
# Nevertheless, it's performing long I/O operations: it reads and writes cache files on the hard disk. 
# Hence, it will block the process and won't be able to answer other requests while this is happening.
# To solve this, FastAPI implements a neat mechanism: if you define a path operation function or a dependency as a standard, non-async function, it'll run it in a separate thread.
# This means that blocking operations, such as synchronous file reading, won't block the main process. 
# In a sense, we could say that it mimics an asynchronous operation.

# To understand this, we'll perform a simple experiment. 
# In the following example, we are building a dummy FastAPI application with three endpoints:
# • /fast, which directly returns a response.
# • /slow-async, a path operation defined as async, which makes a synchronous blocking operation that takes 10 seconds to run.
# • /slow-sync, a path operation that's defined as a standard method, which makes a synchronous blocking operation that takes 10 seconds to run:

app = FastAPI()


@app.get("/fast")
async def fast():
    return {"endpoint": "fast"}


@app.get("/slow-async")
async def slow_async():
    """Runs in the main process"""
    time.sleep(10)  # Blocking sync operation
    return {"endpoint": "slow-async"}


@app.get("/slow-sync")
def slow_sync():
    """Runs in a thread"""
    time.sleep(10)  # Blocking sync operation
    return {"endpoint": "slow-sync"}

# With this simple application, the goal is to see how those blocking operations block the
# main process. 
# Let's run this application with Uvicorn:
# $ uvicorn async_not_async:app

# Next, open two new terminals. In the first one, make a request to the /slow-async endpoint:
# $ http GET http://localhost:8000/slow-async

# Without waiting for the response, in the second terminal, make a request to the /fast endpoint:
# $ http GET http://localhost:8000/fast

# You'll see that you have to wait 10 seconds before you get the response for the /fast endpoint. 
# This means that /slow-async blocked the process and prevented the server for answering the other request while this was happening.

# Now, let's perform the same experiment with the /slow-sync endpoint:
# $ http GET http://localhost:8000/slow-sync

# And again, run the following command:
# $ http GET http://localhost:8000/fast

# You'll immediately get /fast as a response, without having to wait for /slow-sync to finish. 
# Since it's defined as a standard, non-async function, FastAPI will run it in a thread to prevent blocking. 
# However, bear in mind that sending the task to a separate thread implies a small overhead, so it's important to think about the best approach for your current problem.

# So, when developing with FastAPI, how can you choose between standard or async functions for path operations and dependencies? 
# The rules of thumb for this are as follows:
# • If it's not making long I/O operations (file reading, network requests, and so on), define them as async.
# • If you are making I/O operations, do the following:
    # a. Try to choose libraries that are compatible with asynchronous I/O, as we saw for databases or HTTP clients. 
        # In this case, your functions will be async.
    # b. If it's not possible, which is the case for Joblib caching, define them as standard functions. 
        # FastAPI will run them in a separate thread.

# Since Joblib is completely synchronous at making I/O operations, we switched the path operations and the dependency method so that they're synchronous, standard methods.
# In this example, the difference is not very noticeable because the I/O operations are small and fast. 
# However, it's good to keep this in mind if you have to implement slower operations, such as for performing file uploads to cloud storage.