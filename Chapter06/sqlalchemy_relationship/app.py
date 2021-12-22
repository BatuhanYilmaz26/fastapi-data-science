from typing import List, Mapping, Tuple, cast

from databases import Database
from fastapi import Depends, FastAPI, HTTPException, Query, status

from Chapter06.sqlalchemy_relationship.database import get_database, sqlalchemy_engine
from Chapter06.sqlalchemy_relationship.models import (
    comments,
    metadata,
    posts,
    CommentCreate,
    CommentDB,
    PostDB,
    PostCreate,
    PostPartialUpdate,
    PostPublic,
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await get_database().connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


# Earlier, we mentioned that we wanted to retrieve a post and its comments at the same time. 
# To do this, we'll have to make a second query to retrieve the comments and then merge all the data together in a PostPublic instance. 
# We added this logic in the get_post_or_404 dependency, as you can see in the following example:

async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostPublic:
    select_post_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_post_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    select_post_comments_query = comments.select().where(comments.c.post_id == id)
    raw_comments = await database.fetch_all(select_post_comments_query)
    comments_list = [CommentDB(**comment) for comment in raw_comments]

    return PostPublic(**raw_post, comments=comments_list)

# Here, you can see that we simply add a fetch_all query with the correct WHERE statement to collect the comments associated with the post. 
# Then, we only have to transform them into a list of CommentDB and set it during PostPublic initialization.


@app.get("/posts")
async def list_posts(
    pagination: Tuple[int, int] = Depends(pagination),
    database: Database = Depends(get_database),
) -> List[PostDB]:
    skip, limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows = await database.fetch_all(select_query)

    results = [PostDB(**row) for row in rows]

    return results


@app.get("/posts/{id}", response_model=PostPublic)
async def get_post(post: PostPublic = Depends(get_post_or_404)) -> PostPublic:
    return post


@app.post("/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, database: Database = Depends(get_database)
) -> PostPublic:
    insert_query = posts.insert().values(post.dict())
    post_id = await database.execute(insert_query)

    post_db = await get_post_or_404(post_id, database)

    return post_db


@app.patch("/posts/{id}", response_model=PostPublic)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostPublic = Depends(get_post_or_404),
    database: Database = Depends(get_database),
) -> PostPublic:
    update_query = (
        posts.update()
        .where(posts.c.id == post.id)
        .values(post_update.dict(exclude_unset=True))
    )
    post_id = await database.execute(update_query)

    post_db = await get_post_or_404(post_id, database)

    return post_db


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: PostPublic = Depends(get_post_or_404),
    database: Database = Depends(get_database),
):
    delete_query = posts.delete().where(posts.c.id == post.id)
    await database.execute(delete_query)


@app.post("/comments", response_model=CommentDB, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreate, database: Database = Depends(get_database)
) -> CommentDB:
    select_post_query = posts.select().where(posts.c.id == comment.post_id)
    post = await database.fetch_one(select_post_query)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post {id} does not exist"
        )

    insert_query = comments.insert().values(comment.dict())
    comment_id = await database.execute(insert_query)

    select_query = comments.select().where(comments.c.id == comment_id)
    raw_comment = cast(Mapping, await database.fetch_one(select_query))

    return CommentDB(**raw_comment)

# Note that the endpoint parameters and most of the implementations are very close to the create post endpoint. 
# The only difference here is the first part of the function logic where we check for the existence of the post before proceeding with the comment creation. 
# This is important because, since the end user can send any post ID, we could have a situation where we try to create a comment 
    # for a post that doesn't exist, which could cause a constraint error at the database level. 
# This is why we are trying to get the post first and then show a clear error to prevent this situation.