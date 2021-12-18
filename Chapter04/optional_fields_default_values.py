from typing import Optional
from pydantic import BaseModel

# Optional fields and default values
# Up to now, we've assumed that each field had to be provided when instantiating the model. 
# Quite often, however, there are values that we want to be optional because they may not be relevant for each object instance. 
# Sometimes, we also wish to set a default value for a field when it's not specified.
# As you may have guessed, this is done quite simply, with the Optional typing annotation, as illustrated in the following code sample:


class UserProfile(BaseModel):
    nickname: str
    location: Optional[str] = None
    subscribed_newsletter: bool = True


user = UserProfile(nickname="jdoe")
print(user) # nickname='jdoe' location=None subscribed_newsletter=True

# When defining a field with the Optional type hint, it accepts a None value. 
# As you see in the preceding code sample, the default value can be simply assigned by putting the value after an equals sign.

# Be careful, though: don't assign default values such as this for dynamic types such as datetimes.
# By doing so, the datetime instantiation will be evaluated only once when the model is imported. 
# The effect of this is that all the objects you'll instantiate will then share the same value instead of having a fresh value. 
# You can observe this behavior in the following example --> optional_fields_default_values2.py