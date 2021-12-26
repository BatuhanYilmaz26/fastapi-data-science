from os import stat
from typing import cast

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import timezone
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist, IntegrityError

from Chapter07.authentication.password import get_password_hash
from Chapter07.authentication.authentication import authenticate, create_access_token
from Chapter07.authentication.models import (
    AccessTokenTortoise,
    User,
    UserCreate,
    UserDB,
    UserTortoise,
)

app = FastAPI()


# Securing endpoints with access tokens
# Previously, we learned how to implement a simple dependency to protect an endpoint with a header. 
# Here, we'll also retrieve a token from a request header, but then, we'll have to check the database to see if it's valid. 
# If it is, we'll be able to return the corresponding user.
# Let's see what our dependency looks like:

async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")),
) -> UserTortoise:
    try:
        access_token: AccessTokenTortoise = await AccessTokenTortoise.get(
            access_token=token, expiration_date__gte=timezone.now()
        ).prefetch_related("user")
        return cast(UserTortoise, access_token.user)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

# The first thing to notice is that we used the OAuth2PasswordBearer dependency from FastAPI. 
# It goes hand in hand with OAuth2PasswordRequestForm.
# It not only checks for the access token in the Authorization header, but it also informs the OpenAPI schema that the endpoint to get a fresh token is /token.
# This is the purpose of the tokenUrl argument. 
# This is how the automatic documentation can automatically call the access token endpoint in the login form.
# Then we performed a database query with Tortoise. 
# We applied two clauses: one to match the token we got and another to ensure that the expiration date is in the future.
# The __gte syntax is a filter modifier: it allows us to specify the comparison operator to apply when comparing values. 
# Here, gte means "greater than or equal to." 
# You can find a list of every filter that's available in Tortoise in the official documentation: https://tortoise-orm.readthedocs.io/en/latest/query.html#filtering.
# Notice that we also prefetched the related user so that we can directly return it. 
# However, if no corresponding record is found in the database, we raise a 401 error.


# Implementing registration routes

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)

    try:
        user_tortoise = await UserTortoise.create(
            **user.dict(), hashed_password=hashed_password
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    return User.from_orm(user_tortoise)

# As you can see, we are calling get_password_hash on the input password before inserting the user into the database thanks to Tortoise. 
# Note that we are catching a possible IntegrityError exception, which means we're trying to insert an email that already exists.
# Also, notice that we took care to return the user with the User model, not the UserDB model. 
# By doing this, we're ensuring that hashed_password is not part of the output.
# Even hashed, it's generally not advised to leak it into the API responses.


# Implementing a login endpoint
# Now, let's think about the login endpoint. 
# Its goal is to take credentials in the request payload, retrieve the corresponding user, check the password, and generate a new access token. 
# Its implementation is quite straightforward, apart from one thing: the model that's used to handle the request. 
# You'll see why thanks to the following example:

@app.post("/token")
async def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
):
    email = form_data.username
    password = form_data.password
    user = await authenticate(email, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = await create_access_token(user)

    return {"access_token": token.access_token, "token_type": "bearer"}


@app.get("/protected-route", response_model=User)
async def protected_route(user: UserDB = Depends(get_current_user)):
    return User.from_orm(user)


TORTOISE_ORM = {
    "connections": {"default": "sqlite://Chapter07_authentication.db"},
    "apps": {
        "models": {
            "models": ["Chapter07.authentication.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)