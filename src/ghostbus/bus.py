from typing import Protocol


class MessageBus(Protocol):
    async def deliver(self, license_key: str, message: str) -> int:
        """Send message to every connection for license_key. Return recipient count."""
