from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

# Changing the status code of the RedirectResponse class.

app = FastAPI()

@app.get("/redirect")
async def redirect():
    return RedirectResponse("/new-url", status_code=status.HTTP_301_MOVED_PERMANENTLY)