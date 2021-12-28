from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get():
    return {"detail": "GET response"}


@app.post("/")
async def post(request: Request):
    json = await request.json()
    return {"detail": "POST response", "input_payload": json}

# A middleware is a special class that adds global logic to an ASGI application performing things before the request is handled by your path operation functions, 
    # and also after to possibly alter the response. 
# FastAPI provides the add_middleware method for wiring such middleware into your application.
# Here, CORSMiddleware will catch preflight requests sent by the browser and return the appropriate response with the CORS headers corresponding to your configuration. 
# You can see that there are options to finely tune the CORS policy to your needs.
# The most important one is probably allow_origins, which is the list of origins allowed to make requests to your API. 
# Since our HTML application is served from http://localhost:9000, this is what we put here in this argument. 
# If the browser tries to make requests from any other origin, it will stop as it's not authorized to do so by CORS headers.

# The other interesting argument is allow_credentials. 
# By default, browsers don't send cookies for cross-origin HTTP requests. 
# If we wish to make authenticated requests to our API, we need to allow this via this option.

# We can also finely tune the allowed methods and headers that are sent in the request.
# You can find a complete list of arguments for this middleware in the official Starlette documentation: https://www.starlette.io/middleware/#corsmiddleware.