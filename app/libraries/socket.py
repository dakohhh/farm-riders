import socketio
from ..models.user import User
from ..services.token import TokenService
from ..utils.exceptions import ForbiddenException
from pydantic import BaseModel
from typing import Any, Optional


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])



class Location(BaseModel):
    latitude: float
    longitude: float

    class Config:
        allow_mutation = True  # Allow updates




class Connection(BaseModel):
    sid: str
    user: Any
    location: Optional[Location] = None

    class Config:
        allow_mutation = True  # Allow updates





class SocketMemoryDatabase():

    def __init__(self) -> None:
        self.connections: dict = {}

    
    def connect(self, sid:str, user:User):

        connection = Connection(sid=sid, user=user)

        self.connections[sid] = connection

        print(self.connections)

    def update_user_location(self, sid:str, location:Location):

        self.connections[sid].location = location




# latitude=6.5568768 longitude=3.3488896
socket_database = SocketMemoryDatabase()
        


@sio.event
async def connect(sid, environ, auth):
    try:
        headers = environ.get('HTTP_AUTHORIZATION', '')
        token = headers.split(" ")[-1] if headers.startswith('Bearer ') else None

        user_id = await TokenService.verify_auth_token(token)

        user = User.objects.filter(id=user_id).first()

        if not user:
            await sio.disconnect(sid)  # Disconnect the user, invalid token

        socket_database.connect(sid, user)
        
        print(f"Client {sid} connected")

    except ForbiddenException as e:
        print(e)
        await sio.disconnect(sid)

@sio.event
async def message(sid, data):
    print(f"Message received: {data}")

    await sio.send(sid, f"Message received: {data}")

@sio.event
async def private_message(sid, data):

    print(data)

@sio.event
async def update_user_location(sid, data):

    location = Location(**data)
    socket_database.update_user_location(sid, location)

@sio.event
async def disconnect(sid):

    socket_database.connections.pop(sid, None)

    print(f"Client {sid} disconnected")



