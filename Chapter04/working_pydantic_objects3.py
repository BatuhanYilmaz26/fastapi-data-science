from datetime import date
from enum import Enum
from typing import List
from pydantic import BaseModel

# In addition to the previous example (working_pydantic_objects2.py), 
# If you use a conversion quite often, it can be interesting to put it in a method 
    # so that you can reuse it at will, as illustrated in the following example:


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

    def name_dict(self):
        return self.dict(include={"first_name", "last_name"})


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

name_dictionary = person.name_dict()
print(name_dictionary) # {"first_name": "John", "last_name": "Doe"}