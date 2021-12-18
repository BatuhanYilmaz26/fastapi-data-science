from pydantic import BaseModel

# Standard field types
# We'll begin by defining fields with standard types, which only involve simple type hints.
# Let's review a simple model representing information about a person. 
# You can see this in the following code sample:


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int


person = Person(first_name="Batuhan", last_name="Yilmaz", age=23)
print(person)