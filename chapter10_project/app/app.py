from typing import List, Tuple
from fastapi import Depends, FastAPI, Query, status
from tortoise.contrib.fastapi import register_tortoise

from app.models import(
    PostDB,
    PostCreate,
    PostPartialUpdate,
    PostTortoise,
)
from app.settings import Settings

settings = Settings()
app = FastAPI()


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


async def get_post_or_404(id: int) -> PostTortoise:
    return await PostTortoise.get(id=id)


@app.get("/posts")
async def list_posts(pagination: Tuple[int, int] = Depends(pagination)) -> List[PostDB]:
    skip, limit = pagination
    posts = await PostTortoise.all().offset(skip).limit(limit)

    results = [PostDB.from_orm(post) for post in posts]

    return results


@app.get("/posts/{id}", response_model=PostDB)
async def get_post(post: PostTortoise = Depends(get_post_or_404)) -> PostDB:
    return PostDB.from_orm(post)


@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate) -> PostDB:
    post_tortoise = await PostTortoise.create(**post.dict())

    return PostDB.from_orm(post_tortoise)


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


@app.on_event("startup")
async def startup():
    if settings.debug:
        print(settings)


TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": ["app.models"],
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

# You can use settings like any other object in your Python code. 
# If you run this application via uvicorn: $ uvicorn app.app:app
# You'll likely get field required error.

# If one value is missing in your environment, Pydantic will raise an error and the application won't start. 
# Let's set those variables and try again:
# $ export DEBUG="true" ENVIRONMENT="development" DATABASE_URL="sqlite://chapter10_project.db"
# $ uvicorn app.app:app

# The application started! You can even see that our startup event handler printed our settings values. 
# Notice that Pydantic is case-insensitive (by default) when retrieving environment variables. 
# By convention, environment variables are usually set in all caps on the system.