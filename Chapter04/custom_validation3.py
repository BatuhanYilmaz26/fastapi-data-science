from typing import List
from pydantic import BaseModel, validator

# Applying validation before Pydantic parsing
# By default, your validators are run after Pydantic has done its parsing work. 
# This means that the value you get already conforms to the type of field you specified. 
# If the type is incorrect, Pydantic raises an error without calling your validator.

# However, you may sometimes wish to provide some custom parsing logic that allows you to transform input values that would have been incorrect for the type you set. 
# In that case, you would need to run your validator before the Pydantic parser: this is the purpose of the pre argument on validator.

# In the following example, we show how to transform a string with values separated by a comma into a proper list:


class Model(BaseModel):
    values: List[int]

    @validator("values", pre=True)
    def split_string_values(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v


m = Model(values="1,2,3")
print(m.values) # [1, 2, 3]

# You see here that our validator first checks whether we have a string. 
# If we do, we split a comma-separated string and return the resulting list; otherwise, we directly return the value. 
# Pydantic will run its parsing logic after, so you can still be sure that an error will be raised if v is an invalid value.