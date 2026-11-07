from ghostbus.payload import ClientPayload
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
        self.emits: list[tuple[str, object, str]] = []

    async def emit(self, event: str, data: object, *, room: str) -> None:
        self.emits.append((event, data, room))


async def test_deliver_emits_json_payload_to_license_room() -> None:
    sio = FakeSocketIO(sids=["a", "b"])
    payload = ClientPayload(message="Hello World", data="123456")
    delivered = await SocketIOBus(sio).deliver("abc123", payload)
    assert delivered == 2
    assert sio.emits == [
        ("message", {"message": "Hello World", "data": "123456"}, "abc123")
    ]


async def test_deliver_omits_data_when_absent() -> None:
    sio = FakeSocketIO(sids=["a"])
    delivered = await SocketIOBus(sio).deliver(
        "abc123", ClientPayload(message="Hello World")
    )
    assert delivered == 1
    assert sio.emits == [("message", {"message": "Hello World"}, "abc123")]


async def test_deliver_counts_zero_when_room_is_empty() -> None:
    sio = FakeSocketIO(sids=[])
    delivered = await SocketIOBus(sio).deliver(
        "abc123", ClientPayload(message="Hello World", data="123456")
    )
    assert delivered == 0
    assert sio.emits == []
