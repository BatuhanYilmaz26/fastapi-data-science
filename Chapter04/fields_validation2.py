from datetime import date, datetime
from typing import List
from pydantic import BaseModel, Field

# Dynamic default values
# In the previous section, we warned you about setting dynamic values as defaults.
# Fortunately, Pydantic provides the default_factory argument on the Field function to cover this use case. 
# This argument expects you to pass a function that will be called during model instantiation. 
# Thus, the resulting object will be evaluated at runtime each time you create a new object. 
# You can see how to use it in the following example:

def list_factory():
    return ["a", "b", "c"]


class Model(BaseModel):
    l: List[str] = Field(default_factory=list_factory)
    d: datetime = Field(default_factory=datetime.now)
    l2: List[str] = Field(default_factory=list)


# You simply have to pass a function to this argument. 
# Don't put arguments on it—it'll be Pydantic that will automatically call the function for you when instantiating a new object.
# If you need to call a function with specific arguments, you'll have to wrap it into your own function, as we did for list_factory.

# Notice also that the first positional argument used for the default value (such as None or ...) is completely omitted here. 
# This makes sense: it's not consistent to have both a default value and a factory. 
# Pydantic will raise an error if you set those two arguments together.

o1 = Model()
print(o1.l)  # ["a", "b", "c"]
print(o1.l2)  # []

o1.l.append("d")
print(o1.l)  # ["a", "b", "c", "d"]

o2 = Model()
print(o2.l)  # ["a", "b", "c"]
print(o1.l2)  # []

print(o1.d < o2.d)  # True