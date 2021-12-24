from typing import List, Tuple

from fastapi import Depends, FastAPI, Query, status
from tortoise.contrib.fastapi import register_tortoise

from Chapter06.tortoise.models import (
    PostDB,
    PostCreate,
    PostPartialUpdate,
    PostTortoise,
)

app = FastAPI()

async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


async def get_post_or_404(id: int) -> PostTortoise:
    return await PostTortoise.get(id=id)

# The role of this dependency is to take the id in the path parameter and retrieve a single object from the database that corresponds to this identifier. 
# The get method is a convenient shortcut for this: if no matching record is found, it raises the DoesNotExist exception. 
# If there is more than one matching record, it raises MultipleObjectsReturned.
# You might be wondering where our exception handler is to raise a proper 404 error.
# In fact, it's already there, at a global level! Remember that we set up Tortoise with the add_exception_handlers option: under the hood, 
    # it adds a handler that automatically catches DoesNotExist and builds a proper 404 error. 
# So, we don't have to do anything more!


# Getting and filtering objects
# Usually, a REST API provides two types of endpoints to read data: one to list objects and one to get a specific object. 
# This is exactly what we'll review next!
# In the following example, you can see how we implemented the endpoint to list objects:

@app.get("/posts")
async def list_posts(pagination: Tuple[int, int] = Depends(pagination)) -> List[PostDB]:
    skip, limit = pagination
    posts = await PostTortoise.all().offset(skip).limit(limit)

    results = [PostDB.from_orm(post) for post in posts]

    return results

# This is an operation in two steps: first, we retrieve Tortoise objects using the query language. 
# Notice that we use the all method, which gives us every object in the table. 
# Additionally, we're able to apply our pagination parameters through offset and limit.
# Then, we have to transform this list of PostTortoise objects into a list of PostDB objects. 
# Thanks to from_orm and a list comprehension, we can do this very easily.


# Now, in the following example, we'll take a look at the endpoint to retrieve a single post:

@app.get("/posts/{id}", response_model=PostDB)
async def get_post(post: PostTortoise = Depends(get_post_or_404)) -> PostDB:
    return PostDB.from_orm(post)

# This is a simple GET endpoint that expects the ID of the post in the path parameter.
# The implementation is itself very light: we just have to transform our PostTortoise object into a PostDB. 
# Most of the logic is in the get_post_or_404 dependency, which we'll reuse often in our application.


# Creating objects
# Let's start by inserting new objects inside our database. 
# The main challenge is to transform the Tortoise object instance into a Pydantic model. 
# Let's review this in the following example:

@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate) -> PostDB:
    post_tortoise = await PostTortoise.create(**post.dict())

    return PostDB.from_orm(post_tortoise)

# Here, we have our POST endpoint, which accepts our PostCreate model. 
    # The core logic consists then of two operations.
# First, we create the object in the database. We directly use the PostTortoise class and its static create method. 
# Conveniently, it accepts a dictionary that maps fields to their values, so we just have to call dict on our input object. 
# Of course, this operation is natively asynchronous!
# As a result, we get an instance of a PostTortoise object. 
# This is why the second operation we need to perform is to transform it into a Pydantic model. 
# To do this, we use the from_orm method, which is available because we enabled orm_mode.
# We get a proper PostDB instance, which we can return directly.


# Updating and deleting objects 
# The logic is always the same; we just have to adapt the methods we call on our Tortoise object.
# In the following example, you can view the implementation of the update endpoint:
# Here, the main point of attention is that we'll operate directly on the post we want to modify. 
# This is one of the key aspects when working with ORM: entities are objects that can be modified as you wish. 
# When you are happy with the data, you can persist it in the database. 
# This is exactly what we do here: we get a fresh representation of our post thanks to get_post_or_404 
    # and apply the update_from_dict utility method to change the fields that we want. 
# Then, we can persist the changes in the database using save.
# The same concept is applied when you wish to delete an object: 
    # when you have an instance, you can call delete to physically remove it from the database.

@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(
    post_update: PostPartialUpdate, post: PostTortoise = Depends(get_post_or_404)
) -> PostDB:
    post.update_from_dict(post_update.dict(exclude_unset=True))
    await post.save()

    return PostDB.from_orm(post)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: PostTortoise = Depends(get_post_or_404)):
    await post.delete()


# Setting up the Tortoise engine
# Now that we have our model ready, we have to configure the Tortoise engine to set the database connection string and the location of our models. 
# To do this, Tortoise comes with a utility function for FastAPI that does all the required tasks for you. 
# In particular, it automatically adds event handlers to open and close the connection at startup and shutdown; this is something we had to do by hand with SQLAlchemy.
# You can see what it looks like in the following example:

TORTOISE_ORM = {
    "connections": {"default": "sqlite://Chapter06_tortoise.db"},
    "apps": {
        "models": {
            "models": ["Chapter06.tortoise.models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

# As you can see, we put the main configuration options in a variable named TORTOISE_ ORM. 
    # Let's review its different fields:
# • The connections key contains a dictionary associating a database alias to a connection string, which gives access to your database. 
# It follows the standard convention, as explained in the documentation at https://tortoise-orm.readthedocs.io/en/latest/databases.html?highlight=db_url#db-url.
# In most projects, you'll probably have one database named default, but it allows you to set several databases if needed.
# • In the apps key, you'll be able to declare all your modules containing your Tortoise models. 
# The first key just below apps, that is, models, will be the prefix with which you'll be able to refer to the associated models. 
# You can name it how you want, but if you place all your models under the same scope, then models is a good candidate. 
# This prefix is especially important when defining foreign keys.
# For example, with this configuration, our PostTortoise model can be referred to by the name models.PostTortoise. 
# It's not the actual path to your module. 
# Underneath it, you have to list all the modules containing your models.
# Additionally, we set the corresponding database connection with the alias we defined earlier.

# Then, we call the register_tortoise function that'll take care of setting up Tortoise for FastAPI. 
    # Let's explain its arguments:
# • The first one is your FastAPI app instance. 
# • Then, we have the configuration that we defined earlier.
# • Setting generate_schemas to True will automatically create the table's schema in the database. 
# Otherwise, our database will be empty and we won't be able to insert any rows.
# While this is useful for testing purposes, in a real-world application, you should have a proper migration system whose role is to make sure your database schema is in sync. 
# We'll examine how to set one up for Tortoise later in the chapter.
# • Finally, the add_exception_handlers option adds custom exception handlers to FastAPI, allowing you to nicely catch Tortoise errors and return proper error responses.

# And that's all! 
# Always make sure that you call this function at the end of your application file, to ensure everything has been correctly imported. 
# Apart from that, Tortoise handles everything for us. We're now ready to go!