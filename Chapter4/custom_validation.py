from datetime import date
from pydantic import BaseModel, ValidationError, validator

# Adding custom data validation with Pydantic
# Up to now, we've seen how to apply basic validation to our models, through the Field arguments or the custom types provided by Pydantic. 
# In a real-world project, though, you'll probably need to add your own custom validation logic for your specific case.
# Pydantic allows this by defining validators, which are methods on the model that can be applied at a field level or an object level.

# Applying validation at a field level
# This is the most common case: have a validation rule for a single field. 
# To define it in Pydantic, we'll just have to write a static method on our model and decorate it with the validator decorator. 
# As a reminder, decorators are syntactic sugar, allowing the wrapping of a function or a class with common logic, without compromising readability.

# The following example checks a birth date by verifying that the person is not more than 120 years old:


class Person(BaseModel):
    first_name: str
    last_name: str
    birthdate: date

    @validator("birthdate")
    def valid_birthdate(cls, v: date):
        delta = date.today() - v
        age = delta.days / 365
        if age > 120:
            raise ValueError("You seem a bit too old!")
        return v


# Invalid birthdate
try:
    Person(first_name="John", last_name="Doe", birthdate="1800-01-01")
except ValidationError as e:
    print(str(e))

# Valid
person = Person(first_name="John", last_name="Doe", birthdate="1991-01-01")
print(person) # first_name='John' last_name='Doe' birthdate=datetime.date(1991, 1, 1)

# As you see here, the validator is a static class method (the first argument, cls, being the class itself), with the value to validate as the v argument. 
# It's decorated by the validator decorator, which expects the name of the argument to validate as the first argument.

# Pydantic expects two things for this method, detailed as follows:
# • If the value is not valid according to your logic, you should raise a ValueError error with an explicit error message.
# • Otherwise, you should return the value that will be assigned in the model. 
    # Notice that it doesn't need to be the same as the input value: you can very well change it to fit your needs. 