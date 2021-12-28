from typing import cast

from fastapi import Depends, FastAPI, Form, HTTPException, Response, status
from fastapi.security import APIKeyCookie
from starlette.middleware.cors import CORSMiddleware
from starlette_csrf import CSRFMiddleware
from tortoise import timezone
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist, IntegrityError

from Chapter07.csrf.authentication import authenticate, create_access_token
from Chapter07.csrf.models import (
    AccessTokenTortoise,
    User,
    UserCreate,
    UserTortoise,
    UserUpdate,
)
from Chapter07.csrf.password import get_password_hash

TOKEN_COOKIE_NAME = "token"
CSRF_TOKEN_SECRET = "__CHANGE_THIS_WITH_YOUR_OWN_SECRET_VALUE__"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CSRFMiddleware,
    secret=CSRF_TOKEN_SECRET,
    sensitive_cookies={TOKEN_COOKIE_NAME},
    cookie_domain="localhost",
)


# Now, when checking for the authenticated user, we'll just have to retrieve the token from the cookie that was sent in the request. 
# Once again, FastAPI provides a security dependency to help with this called APIKeyCookie. 
# You can see it in the following example:

async def get_current_user(
    token: str = Depends(APIKeyCookie(name=TOKEN_COOKIE_NAME)),
) -> UserTortoise:
    try:
        access_token: AccessTokenTortoise = await AccessTokenTortoise.get(
            access_token=token, expiration_date__gte=timezone.now()
        ).prefetch_related("user")
        return cast(UserTortoise, access_token.user)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/csrf")
async def csrf():
    return None


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


@app.post("/login")
async def login(response: Response, email: str = Form(...), password: str = Form(...)):
    user = await authenticate(email, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = await create_access_token(user)

    response.set_cookie(
        TOKEN_COOKIE_NAME,
        token.access_token,
        max_age=token.max_age(),
        secure=True,
        httponly=True,
        samesite="lax",
    )

# Notice that we used the Secure and HttpOnly flags for the resulting cookie. 
# This ensures that it's sent only through HTTPS connection and that its value can't be read from JavaScript, respectively. 
# While this is not enough to prevent every kind of attack, it's crucial for such sensitive information. 
# Besides, we also set the SameSite flag to lax. It's a quite recent flag that allows us to control how the cookie is sent in a cross-origin context. 
# lax is the default value in most browsers and allows the cookie to be sent to sub-domains of the cookie domain but prevent it for other sites. 
# In a sense, it's designed to be the built-in and standard protection against CSRF.

@app.get("/me", response_model=User)
async def get_me(user: UserTortoise = Depends(get_current_user)):
    return User.from_orm(user)


# Now, let's implement an endpoint that allows us to update the email address of the authenticated user. 
# You can see this in the following example:

@app.post("/me", response_model=User)
async def update_me(
    user_update: UserUpdate, user: UserTortoise = Depends(get_current_user)
):
    user.update_from_dict(user_update.dict(exclude_unset=True))
    await user.save()

    return User.from_orm(user)


TORTOISE_ORM = {
    "connections": {"default": "sqlite://Chapter07_csrf.db"},
    "apps": {
        "models": {
            "models": ["Chapter07.csrf.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
