from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostPublic(PostBase):
    id: int


class PostDB(PostBase):
    id: int
    nb_views: int = 0


# Now, whenever you need to add a field for the whole entity, all you have to do is to add it to the PostBase model.
# It's also very convenient if you wish to define methods on your model. 
# Remember that Pydantic models are regular Python classes, so you can implement as many methods as you wish!