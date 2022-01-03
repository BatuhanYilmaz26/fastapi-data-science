from pydantic import BaseSettings

# To structure a settings model, all you need to do is create a class that inherits from pydantic.BaseSettings. 
# The following example shows a configuration class with a debug flag, an environment name, and a database URL:


class Settings(BaseSettings):
    debug: bool = False
    environment: str
    database_url: str

    class Config:
        env_file = ".env"

# As you can see, creating this class is very similar to creating a standard Pydantic model. 
# We can even define default values, as we did for debug here. 
# The good thing with this model is that it works just like any other Pydantic model: 
    # it automatically parses the values it finds in environment variables and raises an error if one value is missing in your environment. 
# This way, you can ensure you don't forget any values directly when the app starts.
# To use it, we only have to create an instance of this class, as we will see in the next example: app.py