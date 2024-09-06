from contextlib import asynccontextmanager

from .routers.auth import router as auth
from .routers.user import router as user
from .libraries.mongo import connect_to_mongo, disconnect_from_mongo
from .utils.rate_limiter import limiter
from .middleware.exceptions import configure_error_middleware
from .middleware.process import configure_processes_middleware

from fastapi import FastAPI, Request



@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        await connect_to_mongo()
        # await insert_food_items_on_startup()
        yield
    finally:
        await disconnect_from_mongo()


app = FastAPI(title="Farm Riders Python Implementation", lifespan=lifespan)

configure_processes_middleware(app)

configure_error_middleware(app)


app.state.limiter = limiter


app.include_router(auth)
app.include_router(user)

@app.get("/")
def home(request: Request):
    return {"version": "0.1", "name": "Farm Riders Python Implementation"}
