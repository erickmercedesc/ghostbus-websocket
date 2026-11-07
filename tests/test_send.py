from fastapi.testclient import TestClient

from ghostbus.app import create_http_app
from ghostbus.bus import MessageBus


class RecordingBus(MessageBus):
    def __init__(self, recipients: int) -> None:
        self.recipients = recipients
        self.calls: list[tuple[str, str]] = []

    async def deliver(self, license_key: str, message: str) -> int:
        self.calls.append((license_key, message))
        return self.recipients


def test_send_delivers_message_to_license() -> None:
    bus = RecordingBus(recipients=2)
    client = TestClient(create_http_app(bus))

    response = client.post("/send", json={"to": "abc123", "message": "Hello World"})

    assert response.status_code == 200
    assert response.json() == {"delivered": 2}
    assert bus.calls == [("abc123", "Hello World")]


def test_send_reports_when_license_is_not_connected() -> None:
    client = TestClient(create_http_app(RecordingBus(recipients=0)))

    response = client.post("/send", json={"to": "missing", "message": "Hello World"})

    assert response.status_code == 404
    assert response.json() == {"detail": "license not connected"}
