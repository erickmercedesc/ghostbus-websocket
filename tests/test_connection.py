from ghostbus.connection import accept_connection


class FakeServer:
    def __init__(self) -> None:
        self.rooms: list[tuple[str, str]] = []

    async def enter_room(self, sid: str, room: str) -> None:
        self.rooms.append((sid, room))


async def test_connect_joins_license_room() -> None:
    sio = FakeServer()
    accepted = await accept_connection(
        sio, "sid-1", {"HTTP_X_LICENSE_KEY": "abc123"}
    )
    assert accepted is True
    assert sio.rooms == [("sid-1", "abc123")]


async def test_connect_without_license_is_rejected() -> None:
    sio = FakeServer()
    accepted = await accept_connection(sio, "sid-1", {})
    assert accepted is False
    assert sio.rooms == []
