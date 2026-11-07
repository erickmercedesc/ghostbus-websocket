from typing import Protocol

from ghostbus.payload import ClientPayload


class MessageBus(Protocol):
    async def deliver(self, license_key: str, payload: ClientPayload) -> int:
        """Send payload to every connection for license_key. Return recipient count."""
