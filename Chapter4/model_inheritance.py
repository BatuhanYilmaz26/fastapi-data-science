from pydantic import BaseModel

# Creating model variations with class inheritance 
# In Chapter 3, Developing a RESTful API with FastAPI, we saw a case where we needed to define two variations of a Pydantic model 
    # in order to split between the data we want to store in the backend and the data we want to show to the user. 
# This is a common pattern in FastAPI: 
    # you define one model for creation, 
    # one for the response and 
    # one for the data to store in the database.
# We show this basic approach in the following sample:


class PostCreate(BaseModel):
    title: str
    content: str


class PostPublic(BaseModel):
    id: int
    title: str
    content: str


class PostDB(BaseModel):
    id: int
    title: str
    content: str
    nb_views: int = 0


# We have three models here, covering three situations. These are outlined as follows:
# • PostCreate will be used for a POST endpoint to create a new post. We expect the user to give the title and the content; however, the identifier (ID) will be automatically determined by the database.
# • PostPublic will be used when we retrieve the data of a post. We want its title and content, of course, but also its associated ID in the database.
# • PostDB will carry all the data we wish to store in the database. Here, we also want to store the number of views, but we want to keep this secret to make our own statistics internally.

# You can see here that we are repeating ourselves quite a lot, especially with the title and content fields. 
# In bigger examples with lots of fields and lots of validation options, this could quickly become unmanageable.

# The solution here is to leverage model inheritance to avoid this. 
# The approach is simple: identify the fields that are common to every variation and put them in a model that will be used as a base for every other. 
# Then, you only have to inherit from that model to create your variations and add the specific fields. 
# In the following example, we will see what our previous example looks like with this method: --> model_inheritance2.py