from enum import Enum

import httpx


from forestmq.session import Session
from forestmq.exceptions import ProviderError, SessionError
from forestmq.logger import logger


class Protocol(Enum):
    TCP = 1
    AMQP = 2  # TODO


class Provider:

    protocol: Protocol
    session: Session
    domain: str

    def __init__(self, *, protocol: Protocol, domain: str):
        self.protocol = protocol
        self.domain = domain
        if self.protocol == Protocol.TCP:
            logger.debug("Using TCP protocol")
            self.session = Session(
                domain=domain,
                path="/provider",
            )
        else:
            raise ProviderError("ForestMQ Error: Must use TCP protocol")

    def send_msg_sync(self, message: dict) -> str:
        data = {
            "destroy": False,
            "message": message,
        }
        try:
            resp = self.session.send_msg_sync(message=data)
            self.session.close()
            return resp.json()
        except httpx.RequestError as e:
            raise SessionError(f"FORESTMQ Error: Failed to send message in session") from e

    async def send_msg(self, message: dict) -> str:
        data = {
            "destroy": False,
            "message": message,
        }
        try:
            resp = await self.session.send_msg(message=data)
            return resp.json()
        except httpx.RequestError as e:
            raise SessionError(f"FORESTMQ Error: Failed to send message in session") from e
