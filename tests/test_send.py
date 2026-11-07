from fastapi.testclient import TestClient

from ghostbus.app import create_http_app
from ghostbus.payload import ClientPayload
from tests.support import RecordingBus


def test_send_delivers_payload_to_license() -> None:
    bus = RecordingBus(recipients=2)
    client = TestClient(create_http_app(bus))

    response = client.post(
        "/send",
        json={"to": "abc123", "message": "Hello World", "data": "123456"},
    )

    assert response.status_code == 200
    assert response.json() == {"delivered": 2}
    assert bus.calls == [
        ("abc123", ClientPayload(message="Hello World", data="123456"))
    ]


def test_send_allows_missing_data() -> None:
    bus = RecordingBus(recipients=1)
    client = TestClient(create_http_app(bus))

    response = client.post("/send", json={"to": "abc123", "message": "Hello World"})

    assert response.status_code == 200
    assert bus.calls == [("abc123", ClientPayload(message="Hello World"))]


def test_send_reports_when_license_is_not_connected() -> None:
    client = TestClient(create_http_app(RecordingBus(recipients=0)))

    response = client.post(
        "/send",
        json={"to": "missing", "message": "Hello World", "data": "123456"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "license not connected"}
