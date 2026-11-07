from ghostbus.bus import MessageBus
from ghostbus.payload import ClientPayload


class RecordingBus(MessageBus):
    def __init__(self, recipients: int) -> None:
        self.recipients = recipients
        self.calls: list[tuple[str, ClientPayload]] = []

    async def deliver(self, license_key: str, payload: ClientPayload) -> int:
        self.calls.append((license_key, payload))
        return self.recipients
