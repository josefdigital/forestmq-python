from enum import Enum

import httpx


from forestmq.session import Session
from forestmq.exceptions import ProviderError, SessionError
from forestmq.logger import logger


class Protocol(Enum):
    """
    Supported communication protocols for ForestMQ.

    :cvar TCP: Use the HTTP-based TCP interface.
    :cvar AMQP: (Planned) Use the AMQP protocol.
    """
    TCP = 1
    AMQP = 2  # TODO


class Provider:
    """
    Provider for sending messages to ForestMQ.

    This class abstracts synchronous and asynchronous message delivery
    to a ForestMQ server via the TCP protocol.

    :param protocol: Communication protocol (only TCP is currently supported).
    :param domain: Full domain (e.g., http://localhost:8005) where ForestMQ is running.

    :raises ProviderError: If a non-supported protocol is provided.
    """
    protocol: Protocol
    session: Session
    domain: str

    def __init__(self, *, protocol: Protocol, domain: str):
        """
        Initialize the Provider with the given protocol and domain.

        :param protocol: Communication protocol (must be Protocol.TCP).
        :param domain: Base domain or IP of the ForestMQ server.
        :raises ProviderError: If protocol is not TCP.
        """
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
        """
        Send a message synchronously to the ForestMQ provider endpoint.

        :param message: A dictionary representing the message payload.
        :return: JSON response from the server as a string.
        :raises SessionError: If the HTTP request fails.
        """
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
        """
        Send a message asynchronously to the ForestMQ provider endpoint.

        :param message: A dictionary representing the message payload.
        :return: JSON response from the server as a string.
        :raises SessionError: If the async HTTP request fails.
        """
        data = {
            "destroy": False,
            "message": message,
        }
        try:
            resp = await self.session.send_msg(message=data)
            return resp.json()
        except httpx.RequestError as e:
            raise SessionError(f"FORESTMQ Error: Failed to send message in session") from e
