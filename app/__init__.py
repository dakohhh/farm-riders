import socketio
from pydantic import BaseModel
from typing import Any, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .services.auth import TokenService
from .utils.exceptions import ForbiddenException
from .models.user import User
from .routers.auth import router as auth
from .routers.user import router as user
from .routers.upload import router as upload
from .routers.vehicle import router as vehicle
from .libraries.mongo import connect_to_mongo, disconnect_from_mongo
from .libraries.socket import sio
from .utils.rate_limiter import limiter
from .middleware.exceptions import configure_error_middleware
from .middleware.process import configure_processes_middleware
from fastapi_cors import CORS
from .scripts.vehicle_scrpts import insert_vehicles_on_startup


@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        await connect_to_mongo()
        await insert_vehicles_on_startup()
        yield
    finally:
        await disconnect_from_mongo()


app = FastAPI(title="Farm Riders Python Implementation", lifespan=lifespan)

configure_processes_middleware(app)

configure_error_middleware(app)

app_socketio = socketio.ASGIApp(sio, app)


app.mount("/socket.io", app_socketio)


app.state.limiter = limiter


app.include_router(auth)
app.include_router(user)
app.include_router(upload)
app.include_router(vehicle)


@app.get("/")
def home(request: Request):
    return {"version": "0.1", "name": "Farm Riders Python Implementation"}
