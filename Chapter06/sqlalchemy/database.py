import sqlalchemy
from databases import Database

# Connecting to a database
# Now that our table is ready, we have to set up the connection between our FastAPI app and the database engine. 
# To begin, we'll instantiate several objects, as shown in the following example:

DATABASE_URL = "sqlite:///Chapter06_sqlalchemy.db"
database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)

# Here, you can see that we have set our connection string inside the DATABASE_URL variable. 
# Generally, it consists of the database engine, followed by authentication information and the hostname of the database server. 
# You can find an overview of this format in the official SQLAlchemy documentation at https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls. 
# In the case of SQLite, we simply have to give the path of the file that will store all of the data.

# Then, we instantiate a Database instance using this URL. 
# This is the connection layer provided by the databases library that will allow us to perform asynchronous queries.

# We also define sqlalchemy_engine, which is the standard synchronous connection object provided by SQLAlchemy. 
# You might think that it constitutes an overlap with database, and you would be absolutely right. 
    # We'll clarify why we need it in our example later.

# Then, we define a simple function whose role is to simply return the database instance.
# This is shown in the following example:

def get_database() -> Database:
    return database

# We'll use this function as a dependency to easily retrieve this instance in our path operation functions.

# Now, we need to tell FastAPI to open the connection with the database when it starts the application and then close it when exiting.
# Fortunately, FastAPI provides two special decorators to perform tasks at startup and shutdown, 
    # as we will see in the next example --> app.py