from collections.abc import Mapping
from typing import Protocol

from ghostbus.identity import license_key_from_environ


class RoomServer(Protocol):
    async def enter_room(self, sid: str, room: str) -> None:
        ...


async def accept_connection(
    server: RoomServer,
    sid: str,
    environ: Mapping[str, str],
) -> bool:
    license_key = license_key_from_environ(environ)
    if license_key is None:
        return False
    await server.enter_room(sid, license_key)
    return True
