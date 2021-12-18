from pydantic import BaseModel, EmailStr, ValidationError, root_validator

# Applying validation at an object level
# It happens quite often that the validation of one field is dependent on another—for example, to check if 
    # a password confirmation matches the password or to enforce a field to be required in certain circumstances. 
# To allow this kind of validation, we need to access the whole object data. 
# For this, Pydantic provides the root_validator decorator, which is illustrated in the following code example:


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str

    @root_validator()
    def passwords_match(cls, values):
        password = values.get("password")
        password_confirmation = values.get("password_confirmation")
        if password != password_confirmation:
            raise ValueError("Passwords don't match")
        return values


# Passwords not matching
try:
    UserRegistration(
        email="jdoe@example.com", password="aa", password_confirmation="bb"
    )
except ValidationError as e:
    print(str(e))

# Valid
user_registration = UserRegistration(
    email="jdoe@example.com", password="aa", password_confirmation="aa"
)
print(user_registration) # email='jdoe@example.com' password='aa' password_confirmation='aa'

# The usage of this decorator is similar to the validator decorator. 
# The static class method(cls) is called along with the values argument, which is a dictionary containing all the fields. 
# Thus, you can retrieve each one of them and implement your logic.

# Once again, Pydantic expects two things for this method, outlined as follows:
# • If the values are not valid according to your logic, you should raise a ValueError error with an explicit error message.
# • Otherwise, you should return a values dictionary that will be assigned to the model. 
    # Notice that you could change some values in this dictionary to fit your needs.