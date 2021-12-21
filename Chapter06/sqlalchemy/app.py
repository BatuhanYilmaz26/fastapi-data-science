from os import stat
from typing import List, Tuple

from databases import Database
import databases
from fastapi import Depends, FastAPI, HTTPException, Query, status

from Chapter06.sqlalchemy.database import get_database, sqlalchemy_engine
from Chapter06.sqlalchemy.models import (
    metadata,
    posts,
    PostDB,
    PostCreate,
    PostPartialUpdate,
)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await get_database().connect()
    metadata.create_all(sqlalchemy_engine)

@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()

# Decorating functions with the on_event decorators allows us to trigger some useful logic when FastAPI starts or stops. 
# In this case, we simply call the connect and disconnect methods of the database accordingly. 
# This will ensure that the database connection is open and ready to process requests.

# Additionally, you can see that we call the create_all method on the metadata object.
# This is the same metadata object we defined in the previous section and that we have imported here. 
# The goal of this method is to create the table's schema inside our database.
# If we don't do that, our database would be empty and we wouldn't be able to save or retrieve data. 
# This method is designed to work with a standard SQLAlchemy engine; 
    # this is why we instantiated it earlier. 
# It has no other use in the application.

# However, we only created a schema like this to simplify our example. 
# In a real-world application, you should have a proper migration system whose role is to make sure your database schema is in sync. 
# We'll learn how to set one up for SQLAlchemy later in the chapter.

async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)

#Since the logic of retrieving a post by its id or raising a 404 error if it doesn't exist will be reused many times, 
    # it makes sense to put it in a dependency, get_post_or_404.

async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostDB:
    select_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return PostDB(**raw_post)

# We start by building a SQL query. 
# This time, we have a WHERE clause, which only retrieves the row for the id we need. The clause itself might look strange. 
# The first part is to set the actual column we want to compare. 
# Each column is accessible via its name from the c attribute of the table object, that is, posts.c.id.
# Then, we use the equality operator to compare with our actual id variable. 
# It looks like a standard comparison that would result in a Boolean, not a SQL statement! 
# In a general Python context, it would. However, SQLAlchemy developers have done something clever  here: 
    # they overloaded the standard operators so that they produce SQL expressions instead of comparing objects.
# Then, we simply call fetch_one on the database object. 
# It's a convenient shortcut when we only expect one row at most.
# Two things can happen: if no row matches our query, the result is None.
# In this case, we can raise a 404 error. Otherwise, we get the data in the form of a dictionary. 
# All we have to do is to instantiate it back into a PostDB model.


# Making select queries (select comes after insert)
# Now that we can insert new data into our database, we must be able to read it! 
# Typically, you'll have two kinds of read endpoints in your API: 
    # one to list objects and one to get a single object.
# Let's start with the endpoint to list our blog posts. 
# You can view it in the following example:

@app.get("/posts")
async def list_posts(
    pagination: Tuple[int, int] = Depends(pagination),
    database: Database = Depends(get_database),
) -> List[PostDB]:
    skip, limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows = await database.fetch_all(select_query)

    results = [PostDB(**row) for row in rows]

    return results

# Once again, making a query is a two-step operation: first, we build the query thanks to the SQLAlchemy query language. 
# Then, we execute it asynchronously using database.
# In this case, we perform a SELECT query using the corresponding method on the posts table. 
# Notice how we use the OFFSET and LIMIT clauses to paginate our list of posts using the variables provided by the pagination dependency.
# Then, we execute this query with the fetch_all method of database. 
# This method will return a list of rows that match our query.
# Each row is returned in the form of a dictionary that associates column names and their values. 
# Therefore, for each of them, we simply have to instantiate them back to a PostDB model by unpacking the dictionary.

# The other typical endpoint in a REST API is to get a single object. 
# In the following example, you can see how we implemented this endpoint to retrieve a single post:

@app.get("/posts/{id}", response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post


# Making insert queries
# Now we're ready to make queries! 
# Let's start with the INSERT queries to create new rows in our database. 
# In the following example, you can view an implementation of an endpoint to create a new post:

app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, database: Database = Depends(get_database)
) -> PostDB:
    insert_query = posts.insert().values(post.dict())
    post_id = await database.execute(insert_query)

    post_db = await get_post_or_404(post_id, database)

    return post_db

# You shouldn't be surprised by the look of it: it's a POST endpoint that accepts a payload following the PostCreate model. 
# It also injects the database thanks to our get_ database dependency.
# Interesting things begin in the body of the function:

# • On the first line, we build our INSERT query. 
# Rather than writing SQL queries by hand, we rely on the SQLAlchemy expression language, which consists of chained method calls. 
# Under the hood, SQLAlchemy will build a proper SQL query for our database engine. 
# This is one of the greatest benefits of such libraries: since it produces the SQL query for you, 
    # you won't have to modify your source code if you change your database engine.
# • This query is built directly from the posts object, which is the Table instance that we defined earlier in the models.py file. 
# By using this object, SQLAlchemy directly understands that the query concerns this table and builds the SQL accordingly.
# • We start by calling the insert method. Then, we move ahead with the values method. 
# This simply accepts a dictionary that associates the names of the columns with their values. 
# Hence, we just need to call dict() on our Pydantic object. 
# This is why it's important that our model matches the database schema.
# • On the second line, we'll actually perform the query. 
# Thanks to database, we can execute it asynchronously. 
# For an insert query, we'll use the execute method, which expects the query in an argument.

# An INSERT query will return the id of the newly inserted row. 
# This is very important because, since we allow the database to automatically increment this identifier, 
    # we don't know the id of our new post beforehand.
# In fact, we need it to retrieve this new row from the database afterward. 
# By doing this, we ensure we have an exact representation of the current object in the database before returning it in the response. 
# For this, we used the get_post_or_404 function.

# Making update and delete queries
# Finally, let's examine how to update and delete rows in our database. 
# The main difference is how you build the query using SQLAlchemy expressions, but the rest of the implementation is always the same.
# In the following example, let's take a look at how to update a blog post:

@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostDB = Depends(get_post_or_404),
    database: Database = Depends(get_database),
) -> PostDB:
    update_query = (
        posts.update().where(posts.c.id == post.id).values(post_update.dict(exclude_unset=True))
    )
    post_id = await database.execute(update_query)

    post_db = await get_post_or_404(post_id, database)

    return post_db

# In this case, we start with an UPDATE statement. 
# Upon this, we add a WHERE clause to only match the post we want to update. 
# Finally, we set the values we want to update in the form of a dictionary. 
# As we explained in Chapter 4, Managing pydantic Data Models in FastAPI, since we are doing a partial update here, 
    # you can see that we use the exclude_ unset option to only get the values to update.

# Deleting an object is not very different, as you can see in the following example:

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: PostDB = Depends(get_post_or_404), database: Database = Depends(get_database)
):
    delete_query = posts.delete().where(posts.c.id == post.id)
    await database.execute(delete_query)

# It mainly consists of a DELETE statement followed by the adequate WHERE clause.