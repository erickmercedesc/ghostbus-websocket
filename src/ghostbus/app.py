from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ghostbus.bus import MessageBus

LICENSE_NOT_CONNECTED = "license not connected"


class SendBody(BaseModel):
    to: str = Field(description="X-License-Key of the connected Socket.IO clients")
    message: str = Field(description="Text delivered to every connection of that license")


class SendResult(BaseModel):
    delivered: int = Field(description="How many Socket.IO connections received the message")


class LicenseNotConnected(BaseModel):
    detail: str = Field(default=LICENSE_NOT_CONNECTED)


def create_http_app(bus: MessageBus) -> FastAPI:
    app = FastAPI(
        title="GhostBusSocket",
        description=(
            "HTTP-to-Socket.IO intermediary. "
            "Clients connect with X-License-Key. "
            "POST /send delivers the text to every connection of that license."
        ),
        version="0.1.0",
    )

    @app.post(
        "/send",
        response_model=SendResult,
        responses={
            404: {
                "model": LicenseNotConnected,
                "description": LICENSE_NOT_CONNECTED,
            }
        },
        summary="Send a message to a license",
    )
    async def send(body: SendBody) -> SendResult:
        delivered = await bus.deliver(body.to, body.message)
        if delivered == 0:
            raise HTTPException(status_code=404, detail=LICENSE_NOT_CONNECTED)
        return SendResult(delivered=delivered)

    return app
