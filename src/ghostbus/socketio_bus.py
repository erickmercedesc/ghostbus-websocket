from typing import Protocol

from ghostbus.bus import MessageBus


class SocketIOServer(Protocol):
    manager: object

    async def emit(self, event: str, data: str, *, room: str) -> None:
        ...


class SocketIOBus(MessageBus):
    def __init__(self, server: SocketIOServer) -> None:
        self._server = server

    async def deliver(self, license_key: str, message: str) -> int:
        participants = list(self._server.manager.get_participants("/", license_key))
        if not participants:
            return 0
        await self._server.emit("message", message, room=license_key)
        return len(participants)
