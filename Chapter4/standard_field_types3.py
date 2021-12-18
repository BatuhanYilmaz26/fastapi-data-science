from datetime import date
from enum import Enum
from typing import List
from pydantic import BaseModel, ValidationError


# Standard field types 
# As we have seen in the previous examples we can have quite complex field types.
# But that's not all: fields can be Pydantic models themselves, allowing you to have sub-objects! 
# In the following code example, we expand the previous one to add an address field:


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


# We just have to define another Pydantic model and use it as a type hint. 
# Now, you can either instantiate a Person instance with an already valid Address instance or, even better, with a dictionary. 
# In this case, Pydantic will automatically parse it and validate it against the address model.

# In the following code sample, we try to input an invalid address:
# Invalid address
try:
    Person(
        first_name="John",
        last_name="Doe",
        gender=Gender.MALE,
        birthdate="1991-01-01",
        interests=["travel", "sports"],
        address={
            "street_address": "12 Squirell Street",
            "postal_code": "424242",
            "city": "Woodtown",
            # Missing country
        },
    )
except ValidationError as e:
    print(str(e))

# This will generate a validation error.

# Now let's try it with the valid values.
# Valid
# Valid
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
print(person)
# With the valid values everythin works fine as expected and we get the following output:
# first_name='John' last_name='Doe' gender=<Gender.MALE: 'MALE'> birthdate=datetime.date(1991, 1, 1) 
# interests=['travel', 'sports'] address=Address(street_address='12 Squirell Street', postal_code='424242', city='Woodtown', country='US')