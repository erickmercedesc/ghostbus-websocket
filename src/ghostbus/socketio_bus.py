from typing import Any, Protocol

from ghostbus.bus import MessageBus
from ghostbus.payload import ClientPayload


class SocketIOServer(Protocol):
    manager: object

    async def emit(self, event: str, data: Any, *, room: str) -> None:
        ...


class SocketIOBus(MessageBus):
    def __init__(self, server: SocketIOServer) -> None:
        self._server = server

    async def deliver(self, license_key: str, payload: ClientPayload) -> int:
        participants = list(self._server.manager.get_participants("/", license_key))
        if not participants:
            return 0
        await self._server.emit("message", payload.as_event(), room=license_key)
        return len(participants)
