from ghostbus.bus import MessageBus


class RecordingBus(MessageBus):
    def __init__(self, recipients: int) -> None:
        self.recipients = recipients
        self.calls: list[tuple[str, str]] = []

    async def deliver(self, license_key: str, message: str) -> int:
        self.calls.append((license_key, message))
        return self.recipients
