from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str

    def excerpt(self) -> str:
        return f"{self.content[:140]}..."


class PostCreate(PostBase):
    pass


class PostPublic(PostBase):
    id: int


class PostDB(PostBase):
    id: int
    nb_views: int = 0


# Defining the excerpt method on PostBase means that this will be available in every model variation.
# While not strictly required, this inheritance approach is strongly recommended to avoid code duplication and, ultimately, bugs. 
# We'll see in the next section that it'll make even more sense with custom validation methods. --> custom_validation.py