from datetime import date
from enum import Enum
from typing import List
from pydantic import BaseModel

# Working with Pydantic objects
# When developing API endpoints with FastAPI, you'll likely get a lot of Pydantic model instances to handle. 
# It's then up to you to implement the logic to make a link between those objects and your services, such as your database or your machine learning (ML) model.
# Fortunately, Pydantic provides methods to make this very easy. We'll review common use cases that will be useful for you during development.

# Converting an object into a dictionary
# This is probably the action you'll perform the most on a Pydantic object: convert it to a raw dictionary that'll be easy to send to another API or use in a database, for example.
# You just have to call the dict method on the object instance.

# The following example reuses the Person and Address models we saw in the Standard field types section of this chapter:


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

person_dict = person.dict()
print(person_dict["first_name"]) # "John"
print(person_dict["address"]["street_address"]) # "12 Squirell Street"

# As you see, calling dict is enough to transform the whole data into a dictionary.
# Sub-objects are also recursively converted: the address key points itself to a dictionary with the address properties.