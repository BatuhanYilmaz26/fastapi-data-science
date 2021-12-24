from os import stat
from typing import List, Tuple

from fastapi import Depends, FastAPI, HTTPException, Query, status
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from Chapter06.tortoise_relationship.models import (
    CommentBase,
    CommentDB,
    CommentTortoise,
    PostCreate,
    PostDB,
    PostPartialUpdate,
    PostPublic,
    PostTortoise,
)

app = FastAPI()


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


# Our objective is to output the comments when retrieving a single post. 
# To do this, we made a small change to the get_post_or_404 dependency, as follows:

async def get_post_or_404(id: int) -> PostTortoise:
    try:
        return await PostTortoise.get(id=id).prefetch_related("comments")
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# The only difference here is that we called the prefetch_related method on our query.
# By passing in the name of the related entities, it allows you to preload them upfront when getting the main object. 
# By default, Tortoise is lazy and doesn't make the additional query.
# In our case, it's not just an optimization: it's important to ensure our code is working.
# Indeed, if our validator tries to call list on a query set that hasn't been prefetched, it'll raise an error. 
# This is because of the asynchronous nature of the ORM: you have to retrieve the data asynchronously, 
    # with a proper await statement, before you can operate over the data normally.


@app.get("/posts")
async def list_posts(pagination: Tuple[int, int] = Depends(pagination)) -> List[PostDB]:
    skip, limit = pagination
    posts = await PostTortoise.all().offset(skip).limit(limit)

    results = [PostDB.from_orm(post) for post in posts]

    return results


@app.get("/posts/{id}", response_model=PostPublic)
async def get_post(post: PostTortoise = Depends(get_post_or_404)) -> PostPublic:
    return PostPublic.from_orm(post)


@app.post("/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate) -> PostPublic:
    post_tortoise = await PostTortoise.create(**post.dict())
    await post_tortoise.fetch_related("comments")

    return PostPublic.from_orm(post_tortoise)


@app.patch("/posts/{id}", response_model=PostPublic)
async def update_post(
    post_update: PostPartialUpdate, post: PostTortoise = Depends(get_post_or_404)
) -> PostPublic:
    post.update_from_dict(post_update.dict(exclude_unset=True))
    await post.save()

    return PostPublic.from_orm(post)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: PostTortoise = Depends(get_post_or_404)):
    await post.delete()


@app.post("/comments", response_model=CommentDB, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentBase) -> CommentDB:
    try:
        await PostTortoise.get(id=comment.post_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post {id} does not exist"
        )
    
    comment_tortoise = await CommentTortoise.create(**comment.dict())

    return CommentDB.from_orm(comment_tortoise)

# Most of the logic is very similar to the create post endpoint. 
# The main difference is that we first check for the existence of the post before proceeding with the comment creation.
# Indeed, we want to avoid the foreign key constraint error that could occur at the database level and show a clear and helpful error message to the end user instead.


# Setting up a database migration system with Aerich 
# When you make changes to your database schema, you want to migrate your existing data in production in a safe and reproducible manner. 
# We'll demonstrate how to install and configure Aerich, which is a database migration tool from the creators of Tortoise. 
# We'll start by installing the library: $ pip install aerich
# Once this is done, you'll have access to the aerich command to manage this migration system.
# The first thing you need to do is declare the Aerich models in your Tortoise configuration.
# Indeed, Aerich stores some migration state information in your database. 
# You can view what the configuration looks like in the following example:

TORTOISE_ORM = {
    "connections": {"default": "sqlite://Chapter06_tortoise_relationship.db"},
    "apps": {
        "models": {
            "models": ["Chapter06.tortoise_relationship.models", "aerich.models"],
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

# Then, you can initialize the migration environment, which is a set of files and directories
    # where Aerich will store its configuration and migration files. 
# The command looks like this:
    # $ aerich init -t Chapter06.tortoise_relationship.app.TORTOISE_ORM
# The -t option should refer to the dotted path of your TORTOISE_ORM configuration variable. 
# This is how Aerich is able to retrieve your database connection information and the definition of your models. 
# Then, you have to call the following command:
    # $ aerich init-db
# The migrations folder will contain all of the migration scripts. 
# Notice that it creates a sub-directory for each of the "apps" defined in the configuration. 
# As you can see, we have a first migration script that creates all the tables that have already been defined.

# To apply the migrations to your database, simply run the following command:
    # $ aerich upgrade
# During the life of your project, when you have made changes to your table's schema, you'll have to generate new migration scripts to reflect the changes. 
# This is done quite easily using the following command:
    # $ aerich migrate --name added_new_tables
# The --name option allows you to set a name for your migration. 
# It will automatically generate a new migration file that reflects your changes.