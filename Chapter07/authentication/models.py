from datetime import date, datetime, timedelta
from pydantic import BaseModel, EmailStr, Field
from tortoise.models import Model
from tortoise import fields, timezone
from Chapter07.authentication.password import generate_token

def get_expiration_date(duration_seconds: int = 86400) -> datetime:
    return timezone.now() + timedelta(seconds=duration_seconds)

# Creating models and tables
# The first thing we must do is create the Pydantic models, as shown in the following example:


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


class UserDB(User):
    hashed_password: str


class AccessToken(BaseModel):
    user_id: int
    access_token: str = Field(default_factory=generate_token)
    expiration_date: datetime = Field(default_factory=get_expiration_date)

    class Config:
        orm_mode = True


# To keep this example simple, we're only considering the email address and password in our user model. 
# As you can see, there is a major difference between UserCreate and UserDB: the former accepts the plain text password we'll hash during registration, 
    # while the second will only keep the hashed password in the database.
# Now, we can define the corresponding Tortoise model, as shown in the following example:

class UserTortoise(Model):
    id: fields.IntField(pk=True)
    email = fields.CharField(index=True, unique=True, null=False, max_length=255)
    hashed_password = fields.CharField(null=False, max_length=255)

    class Meta:
        table = "users"

# Note that we added a unique constraint to the email column to ensure we can't have duplicate emails in our database.


class AccessTokenTortoise(Model):
    access_token = fields.CharField(pk=True, max_length=255)
    user = fields.ForeignKeyField("models.UserTortoise", null=False)
    expiration_date = fields.DatetimeField(null=False)

    class Meta:
        table = "access_tokens"