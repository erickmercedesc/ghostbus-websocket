from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ghostbus.bus import MessageBus


class SendBody(BaseModel):
    to: str
    message: str


def create_http_app(bus: MessageBus) -> FastAPI:
    app = FastAPI()

    @app.post("/send")
    async def send(body: SendBody) -> dict[str, int]:
        delivered = await bus.deliver(body.to, body.message)
        if delivered == 0:
            raise HTTPException(status_code=404, detail="license not connected")
        return {"delivered": delivered}

    return app
