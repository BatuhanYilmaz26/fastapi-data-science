from datetime import date
from enum import Enum
from typing import List
from pydantic import BaseModel, ValidationError

# Standard field types 
# We are not limited to scalar types: we can actually use compound types such as lists, tuples, or datetime classes. 
# In the following example, you can see a model using those more complex types:


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"


class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: List[str]


# There are three things to notice in this example. 

# First, we used the standard Python Enum class as a type for the gender field. 
    # This allows us to specify a set of valid values. 
# If we input a value that's not in this enumeration, Pydantic will raise an error, as illustrated in the following example:

# Invalid gender
try:
    Person(
        first_name="John",
        last_name="Doe",
        gender="INVALID_VALUE",
        birthdate="1991-01-01",
        interests=["travel", "sports"],
    )
except ValidationError as e:
    print(str(e))

# If you run the preceding example, you'll get a validation error.

# Then, we used the date Python class as a type for the birthdate field. 
# Pydantic is able to automatically parse dates and datetimes given as an International Organization for Standardization (ISO) 
# format string or a timestamp integer and instantiate a proper date or datetime object. 
# Of course, if the parsing fails, you'll also get an error. 
# You can experiment with this in the following example:

# Invalid birthdate
try:
    Person(
        first_name="John",
        last_name="Doe",
        gender=Gender.MALE,
        birthdate="1991-13-42",
        interests=["travel", "sports"],
    )
except ValidationError as e:
    print(str(e))

# If you run the preceding example, you'll get a validation error.

# Now let's try it with the valid values.
# Valid
person = Person(
    first_name="John",
    last_name="Doe",
    gender=Gender.MALE,
    birthdate="1991-01-01",
    interests=["travel", "sports"],
)

print(person)
# With the valid values everythin works fine as expected and we get the following output:
# first_name='John' last_name='Doe' gender=<Gender.MALE: 'MALE'> birthdate=datetime.date(1991, 1, 1) interests=['travel', 'sports']