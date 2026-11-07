from ghostbus.socketio_bus import SocketIOBus


class FakeManager:
    def __init__(self, sids: list[str]) -> None:
        self._sids = sids

    def get_participants(self, namespace: str, room: str):
        assert namespace == "/"
        return iter(self._sids)


class FakeSocketIO:
    def __init__(self, sids: list[str]) -> None:
        self.manager = FakeManager(sids)
        self.emits: list[tuple[str, str, str]] = []

    async def emit(self, event: str, data: str, *, room: str) -> None:
        self.emits.append((event, data, room))


async def test_deliver_emits_to_license_room() -> None:
    sio = FakeSocketIO(sids=["a", "b"])
    delivered = await SocketIOBus(sio).deliver("abc123", "Hello World")
    assert delivered == 2
    assert sio.emits == [("message", "Hello World", "abc123")]


async def test_deliver_counts_zero_when_room_is_empty() -> None:
    sio = FakeSocketIO(sids=[])
    delivered = await SocketIOBus(sio).deliver("abc123", "Hello World")
    assert delivered == 0
    assert sio.emits == []
