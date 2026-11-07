from pydantic import BaseModel, Field


class ClientPayload(BaseModel):
    message: str = Field(description="Text delivered to every connection of that license")
    data: str | None = Field(
        default=None,
        description="Optional extra payload delivered with the message",
    )

    def as_event(self) -> dict:
        return self.model_dump(exclude_none=True)
