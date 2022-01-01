from datetime import date
from enum import Enum
from typing import List
from pydantic import BaseModel

# While writing unit tests, you'll often need variables and objects several times across your tests, such as in an app instance, as some fake data, and so on. 
# To avoid having to repeat the same things over and over across your tests, pytest proposes an interesting feature: fixtures.

# Reusing test logic by creating fixtures
# When testing a large application, tests tend to become quite repetitive: lots of them will share the same boilerplate code before their actual assertion. 
# Let's consider using Pydantic models to represent a person and their postal address:


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"


class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str


class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: List[str]
    address: Address


# Now, let's say that we want to write tests with some instances of those models. 
# Obviously, it would be a bit annoying to instantiate them in each test, filling them with fake data.
# Fortunately, fixtures allow us to write them in one go. 
# In the next example we'll see how to use them: --> introduction_fixtures_test.py