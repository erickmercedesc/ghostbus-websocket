from fastapi.testclient import TestClient

from ghostbus.app import LICENSE_NOT_CONNECTED, create_http_app
from tests.support import RecordingBus


def test_openapi_documents_send() -> None:
    spec = TestClient(create_http_app(RecordingBus(0))).get("/openapi.json").json()
    send = spec["paths"]["/send"]["post"]
    body = spec["components"]["schemas"]["SendBody"]["properties"]
    assert spec["info"]["title"] == "GhostBusSocket"
    assert "to" in body
    assert "message" in body
    assert "404" in send["responses"]
    assert LICENSE_NOT_CONNECTED in str(send["responses"]["404"])


def test_swagger_ui_is_served() -> None:
    response = TestClient(create_http_app(RecordingBus(0))).get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()
