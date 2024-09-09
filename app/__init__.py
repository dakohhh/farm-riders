import socketio
from pydantic import BaseModel
from typing import Any, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from .services.auth import TokenService
from .utils.exceptions import ForbiddenException
from .models.user import User
from .routers.auth import router as auth
from .routers.user import router as user
from .routers.farmers_and_agg import router as farmers_and_agg
from .libraries.mongo import connect_to_mongo, disconnect_from_mongo
from .libraries.socket import sio
from .utils.rate_limiter import limiter
from .middleware.exceptions import configure_error_middleware
from .middleware.process import configure_processes_middleware



@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        await connect_to_mongo()
        yield
    finally:
        await disconnect_from_mongo()


app = FastAPI(title="Farm Riders Python Implementation", lifespan=lifespan)

app_socketio = socketio.ASGIApp(sio, app)

configure_processes_middleware(app)

configure_error_middleware(app)


app.mount("/socket.io", app_socketio)



app.state.limiter = limiter


app.include_router(auth)
app.include_router(user)


@app.get("/")
def home(request: Request):
    return {"version": "0.1", "name": "Farm Riders Python Implementation"}

