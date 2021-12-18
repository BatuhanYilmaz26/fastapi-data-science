from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError

# Validating email addresses and URLs with Pydantic types
# For convenience, Pydantic provides some classes to use as field types to validate 
    # some common patterns such as email addresses or Uniform Resource Locators (URLs).

# In the following example, we'll use EmailStr and HttpUrl to validate an email address and a HyperText Transfer Protocol (HTTP) URL.
# For EmailStr to work, you'll need an optional dependency, email-validator, which you can install with the following command:
    # $ pip install email-validator
# Those classes work like any other type or class: just use them as a type hint for your field.


class User(BaseModel):
    email: EmailStr
    website: HttpUrl


# In the following example, we check that the email address is correctly validated:
# Invalid email
try:
    User(email="jdoe", website="https://www.example.com")
except ValidationError as e:
    print(str(e))

# This will generate a validation error.

# We also check that the URL is correctly parsed, as follows:
# Invalid URL
try:
    User(email="jdoe@example.com", website="jdoe")
except ValidationError as e:
    print(str(e))

# This will also generate a validation error.

# If you have a look at a valid example, shown next, you'll see that the URL is parsed into an 
    # object, giving you access to the different parts of it, such as the scheme or hostname:
# Valid
user = User(email="jdoe@example.com", website="https://www.example.com")
# email='jdoe@example.com' website=HttpUrl('https://www.example.com', scheme='https', host='www.example.com', tld='com', host_type='domain')
print(user)

# Pydantic provides a quite big set of types that can help you in various situations. 
# We invite you to review a full list of these in the official documentation, at https://pydanticdocs.helpmanual.io/usage/types/#pydantic-types.