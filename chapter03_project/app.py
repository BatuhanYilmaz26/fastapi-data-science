from fastapi import FastAPI

from chapter3_project.routers.posts import router as posts_router
from chapter3_project.routers.users import router as users_router

app = FastAPI()

app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(users_router, prefix="/users", tags=["users"])

# To run this application: 
# Copy the example to the root of your project and run the following command:
# $ uvicorn chapter3_project.app:app

# If you open the interactive documentation at http://localhost:8000/docs,
# you'll see that all the routes are there, grouped by the tags we specified when including the router: