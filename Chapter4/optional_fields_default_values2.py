import time
from datetime import date, datetime
from pydantic import BaseModel


class Model(BaseModel):
    # Don't do this.
    # This example shows you why it doesn't work.
    d: datetime = datetime.now()


o1 = Model()
print(o1.d)

time.sleep(5)  # Wait for 5 seconds

o2 = Model()
print(o2.d)

print(o1.d < o2.d) # False

# Even though we waited for 5 seconds between the instantiation of o1 and o2, the d datetime is the same! 
# This means that the datetime is evaluated once when the class is imported.

# You can have the same kind of problem if you want to have a default list, such as l: List[str] = ["a", "b", "c"]. 
# Notice that this is true for every Python object, not only Pydantic models, so you should bear this in mind.