from datetime import date
from enum import Enum
from typing import List
from pydantic import BaseModel

# In addition to the previous example (working_pydantic_objects.py), 
# the dict method supports some arguments, allowing you to select a subset of properties to be converted. 
# You can either state the ones you want to be included or the ones you want to exclude, as you can see in the following sample:


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


person = Person(
    first_name="John",
    last_name="Doe",
    gender=Gender.MALE,
    birthdate="1991-01-01",
    interests=["travel", "sports"],
    address={
        "street_address": "12 Squirell Street",
        "postal_code": "424242",
        "city": "Woodtown",
        "country": "US",
    },
)

person_include = person.dict(include={"first_name", "last_name"})
print(person_include)  # {"first_name": "John", "last_name": "Doe"}

person_exclude = person.dict(exclude={"birthdate", "interests"})
print(person_exclude)
# {'first_name': 'John', 'last_name': 'Doe', 'gender': <Gender.MALE: 'MALE'>, 
# 'address': {'street_address': '12 Squirell Street', 'postal_code': '424242', 'city': 'Woodtown', 'country': 'US'}}

# The include and exclude arguments expect a set with the keys of the fields you want to include or exclude.

# For nested structures such as address here, you can also use a dictionary to specify 
    # which sub-field you want to include or exclude, as illustrated in the following example:

person_nested_include = person.dict(include={
    "first_name": ...,
    "last_name": ...,
    "address": {"city", "country"},
})

print(person_nested_include)
# {'first_name': 'John', 'last_name': 'Doe', 'address': {'city': 'Woodtown', 'country': 'US'}}

# The resulting address dictionary only contains the city and the country. 
# Notice that when using this syntax, scalar fields such as first_name or last_name have to be associated with the ellipsis ... .