from fastapi import FastAPI, Header

# What is dependency injection?
# Generally speaking, dependency injection is a system able to automatically instantiate objects and the ones they depend on. 
# The responsibility of developers is then to only provide a declaration of how an object should be created, 
    # and let the system resolve all the dependency chains and create the actual objects at runtime.

# FastAPI allows you to declare the objects and variables you wish to have at hand only by declaring them in the path operation function arguments. 
# Actually, we already used dependency injection in the previous chapters. 
# In the following example, we use the Header function to retrieve the user-agent header:

app = FastAPI()

@app.get("/")
async def header(user_agent: str = Header(...)):
    return {"user_agent": user_agent}

# Internally, the Header function has some logic to automatically get the request object, 
    # check for the required header, return its value, or raise an error if it's not present. 
# From the developer's perspective, however, we don't know how it handled the required objects for this operation: 
    # we just ask for the value we need. 
# That's dependency injection.

# Admittedly, you could reproduce this example quite easily in the function body 
    # by picking the user-agent property in the headers dictionary of the Request object. 
# However, the dependency injection approach has numerous advantages over this:
# • The intent is clear: you know what the endpoint expects in the request data without reading the function's code.
# • You have a clear separation of concern between the logic of the endpoint and the more generic logic: 
    # the header retrieval and the associated error handling doesn't pollute the rest of the logic; it's self-contained in the dependency function. 
    # Besides, it can be reused easily in other endpoints.
# • In the case of FastAPI, it's used to generate the OpenAPI schema so that 
    # the automatic documentation can clearly show which parameters are expected for this endpoint.

# Put another way, whenever you need utility logic to retrieve or validate data, make security checks or call external logic 
    # that you'll need several times across your application, a dependency is an ideal choice.

# FastAPI relies heavily on this dependency injection system and encourages developers to use it to implement their building blocks. 
# It may be a bit puzzling if you come from other web frameworks such as Flask or Express, but you'll surely be quickly convinced by its power and relevance.