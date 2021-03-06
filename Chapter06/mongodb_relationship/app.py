from typing import List, Tuple

from bson import ObjectId, errors
from fastapi import Depends, FastAPI, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from Chapter06.mongodb_relationship.models import (
    CommentCreate,
    PostDB,
    PostCreate,
    PostPartialUpdate,
)

app = FastAPI()
motor_client = AsyncIOMotorClient(
    "mongodb://localhost:27017"
)  # Connection to the whole server
database = motor_client["chapter6_mongo_relationship"]  # Single database instance


def get_database() -> AsyncIOMotorDatabase:
    return database


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


async def get_post_or_404(
    id: ObjectId = Depends(get_object_id),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> PostDB:
    raw_post = await database["posts"].find_one({"_id": id})

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return PostDB(**raw_post)


@app.get("/posts")
async def list_posts(
    pagination: Tuple[int, int] = Depends(pagination),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> List[PostDB]:
    skip, limit = pagination
    query = database["posts"].find({}, skip=skip, limit=limit)

    results = [PostDB(**raw_post) async for raw_post in query]

    return results


@app.get("/posts/{id}", response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post


@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, database: AsyncIOMotorDatabase = Depends(get_database)
) -> PostDB:
    post_db = PostDB(**post.dict())
    await database["posts"].insert_one(post_db.dict(by_alias=True))

    post_db = await get_post_or_404(post_db.id, database)

    return post_db


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


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: PostDB = Depends(get_post_or_404),
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    await database["posts"].delete_one({"_id": post.id})


@app.post(
    "/posts/{id}/comments", response_model=PostDB, status_code=status.HTTP_201_CREATED
)
async def create_comment(
    comment: CommentCreate,
    post: PostDB = Depends(get_post_or_404),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> PostDB:
    await database["posts"].update_one(
        {"_id": post.id}, {"$push": {"comments": comment.dict()}}
    )

    post_db = await get_post_or_404(post.id, database)

    return post_db

# This one is slightly different from what we've seen so far. 
# Indeed, instead of making comments a "first-class" resource with their own paths, such as for relational databases, here, we chose to nest it under the path of a single post. 
# The motivation behind this is that, since those comments are designed to be nested under posts, 
    # it doesn't really make sense to consider them as single entities that you can work with independently.
# Since we have the post ID in the path parameter, you can reuse our get_post_or_404 dependency to retrieve the post.
# Then, we trigger an update_one query; this time, using the $push operation. 
# This is a useful operator for adding elements to a list attribute. 
# Operators to remove elements from a list are also available. 
# You can find a description of every update operator in the official documentation at https://docs.mongodb.com/manual/reference/operator/update/.
# And that's it! In fact, we don't even have to modify the rest of our code. 
# Because the comments are included in the whole document, we'll always retrieve them when querying for a post in the database. 
# Besides, our PostDB model now expects a comments attribute, so Pydantic will take care of serializing them automatically.