from typing import List, Tuple

from bson import ObjectId, errors
from fastapi import Depends, FastAPI, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from Chapter06.mongodb.models import (
    PostDB,
    PostCreate,
    PostPartialUpdate,
)

# Connecting to a database
# Now that our models are ready, we can set up the connection with a MongoDB server. 
# This is quite easy and only involves a class instantiation, as shown in the following example:

app = FastAPI()
motor_client = AsyncIOMotorClient(
    "mongodb://localhost:27017"
) # Connection to the whole server
database = motor_client["Chapter06_mongo"] # Single database instance


def get_database() -> AsyncIOMotorClient:
    return database

# Here, you can see that AsyncIOMotorClient simply expects a connection string to your database. 
# Generally, it consists of the scheme, followed by authentication information and the hostname of the database server. 
# You can find an overview of this format in the official MongoDB documentation at https://docs.mongodb.com/manual/reference/connection-string/.

# However, be careful. Contrary to the libraries we've discussed so far, the client instantiated here is not bound to any database, that is, it's only a connection to a whole server. 
# That's why we need the second line to set the database that we want to work upon directly by its key. 
# It's worth noting that MongoDB doesn't require you to create the database upfront: it'll create it automatically if it doesn't exist.


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


async def get_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (errors.InvalidId, TypeError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# Here, we simply retrieve the id string from the path parameters and try to instantiate it back into an ObjectId. 
# If it's not a valid value, we catch the corresponding errors and consider it as a 404 error.


async def get_post_or_404(
    id: ObjectId = Depends(get_object_id),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> PostDB:
    raw_post = await database["posts"].find_one({"_id": id})

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return PostDB(**raw_post)

# The logic is quite similar to what we saw for the list endpoint. 
# This time, however, we call the find_one method with a query to match the post identifier: 
    # the key is the name of the document attribute we want to filter on, and the value is the one we are looking for.
# This method returns the document in the form of a dictionary or None if it doesn't exist.
# In this case, we raise a proper 404 error.
# Finally, we transform it back into a PostDB model before returning it.
# You might have noticed that we got the id through a dependency, get_object_id.
# Indeed, FastAPI will return a string from the path parameter. 
# If we try to make a query with the id in the form of a string, MongoDB will not match with the actual binary IDs.
# That's why we use another dependency that transforms the identifier represented as a string (such as 608d1ee317c3f035100873dc) to a proper ObjectId.


# Getting documents
# Of course, retrieving the data from the database is an important part of the job of a REST API. 
# Now, we'll demonstrate how to implement two classic endpoints, that is, to list posts and get a single post. 
# Let's start with the first one and take a look at its implementation in the following example:

@app.get("/posts")
async def list_posts(
    pagination: Tuple[int, int] = Depends(pagination),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> List[PostDB]:
    skip, limit = pagination
    query = database["posts"].find({}, skip=skip, limit=limit)

    results = [PostDB(**raw_post) async for raw_post in query]

    return results

# The most interesting part is the second line where we define the query. 
# After retrieving the posts collection, we call the find method. 
# The first argument should be the filtering query, following the MongoDB syntax. 
# Since we want every document, we leave it empty. 
# Then, we have keyword arguments that allow us to apply our pagination parameters.
# MongoDB returns us a result in the form of a list of dictionaries, which maps fields to their values. 
# This is why we added a list comprehension construct to transform them back into PostDB instances so that FastAPI can serialize them properly.
# You might have noticed something quite surprising here: contrary to what we do usually, we didn't wait for the query directly. 
# Instead, we added the async keyword to our list comprehension. Indeed, in this case, Motor returns an asynchronous generator. 
# It's the asynchronous counterpart of the classic generator. 
# It works in the same way, aside from the async keyword we have to add when iterating over it.


# Now, let's take a look at the endpoint to retrieve a single post. 
# The following example shows its implementation:

@app.get("/posts/{id}", response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post


# Inserting documents
# We will demonstrate how to implement an endpoint to create posts. 
# Essentially, we just have to insert our Pydantic model that has been transformed into a dictionary:

@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, database: AsyncIOMotorDatabase = Depends(get_database)
) -> PostDB:
    post_db = PostDB(**post.dict())
    await database["posts"].insert_one(post_db.dict(by_alias=True))

    post_db = await get_post_or_404(post_db.id, database)

    return post_db

# Classically, this is a POST endpoint that accepts a payload in the form of a PostCreate model. 
# Additionally, we inject the database instance with the dependency we wrote earlier.
# In the path operation itself, you can see that we start by instantiating a PostDB from the PostCreate data. 
# This is usually a good practice if you only have fields in PostDB that need to be initialized.
# Then, we have the query. 
# To retrieve a collection in our MongoDB database, we simply have to get it by name, like a dictionary. 
# Once again, MongoDB will take care of creating it if it doesn't exist. 
# As you can see, document-oriented databases are much more lightweight regarding schema than relational databases! 
# In this collection, we can call the insert_one method to insert a single document. 
# It expects a dictionary to map fields to their values. 
# Therefore, the dict method of Pydantic objects is once again our friend. 
# However, here, we see something new: we call it with the by_alias argument set to True. 
# By default, Pydantic will serialize the object with the real field name, not the alias name. 
# However, we do need the identifier named as _id in our MongoDB database.
# Using this option, Pydantic will use the alias as a key in the dictionary.
# To ensure we have a true and fresh representation of our document in the dictionary, we retrieve it back from the database thanks to our get_post_or_404 function.


# Updating and deleting documents
# We'll now review the endpoints to update and delete documents. 
# The logic is still the same and only involves building the proper query from the request payload.
# Let's start with the PATCH endpoint, which you can view in the following example:

@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostDB = Depends(get_post_or_404),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> PostDB:
    await database["posts"].update_one(
        {"_id": post.id}, {"$set": post_update.dict(exclude_unset=True)}
    )

    post_db = await get_post_or_404(post.id, database)

    return post_db

# Here, you can see that we use the update_one method to update one document. 
# The first argument is the filtering query and the second one is the actual operation to apply to the document. 
# Once again, it follows the MongoDB syntax: the $set operation allows us to only modify the fields we want to change by passing the update dictionary.


# The DELETE endpoint is even simpler: it's just a single query, as you can see in the following example:

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: PostDB = Depends(get_post_or_404),
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    await database["posts"].delete_one({"_id": post.id})

# The delete_one method expects the filtering query as the first argument.