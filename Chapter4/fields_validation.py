from typing import Optional
from pydantic import BaseModel, Field, ValidationError

# Pydantic provides a Field function that allows us to set some advanced options on our fields, including one to set a factory for creating dynamic values. 
    # Before showing you this, we'll first introduce the Field function.

# Field validation
# In Chapter 3, Developing a RESTful API with FastAPI, we showed how to apply some validation to the request parameters 
    # to check if a number was in a certain range or if a string was matching a regular expression (regex). 
# Actually, those options directly come from Pydantic! 
# We can use the same ones to apply validation to the fields of a model.
# To do this, we'll use the Field function from Pydantic and use its result as the default value of the field. 

# In the following example, we define a Person model with the first_name and last_name required properties, 
    # which should be at least three characters long, and an optional age property, which should be an integer between 0 and 120. 
# We show the implementation of this model in the following code sample:


class Person(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    age: Optional[int] = Field(None, ge=0, le=120)


# Invalid first name
try:
    Person(first_name="J", last_name="Doe", age=30)
except ValidationError as e:
    print(str(e))


# Invalid age
try:
    Person(first_name="John", last_name="Doe", age=2000)
except ValidationError as e:
    print(str(e))


# Valid
person = Person(first_name="John", last_name="Doe", age=30)
print(person)  # first_name='John' last_name='Doe' age=30

# As you see, the syntax is very similar to the one we saw for Path, Query, and Body.
# The first positional argument defines the default value for the field. 
# If the field is required, we use the ellipsis ... . 
# Then, the keyword arguments are there to set options for the field, including some basic validation.