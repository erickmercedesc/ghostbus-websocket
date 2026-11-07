import socketio

from ghostbus.app import create_http_app
from ghostbus.connection import accept_connection
from ghostbus.socketio_bus import SocketIOBus

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
http_app = create_http_app(SocketIOBus(sio))


@sio.event
async def connect(sid: str, environ: dict, _auth: object | None = None) -> bool:
    return await accept_connection(sio, sid, environ)


app = socketio.ASGIApp(sio, other_asgi_app=http_app)
