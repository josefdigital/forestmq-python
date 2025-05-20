import asyncio
from typing import Callable

import httpx

from forestmq.exceptions import ConsumerError
from forestmq.logger import logger


class Consumer:
    """
    ForestMQ Consumer for polling messages from a queue endpoint.

    Periodically polls the ForestMQ server at the given interval and
    invokes a user-defined callback with the message content.

    Example:

        def callback(message: dict) -> None:
            print(f"Consumer message: {message['message']}")

        fmq = ForestMQ(domain="http://localhost:8005", interval=1)
        asyncio.run(fmq.consumer.poll(callback))

    :param domain: The domain or IP where the ForestMQ server is hosted.
    :param interval: Polling interval in seconds.
    """

    domain: str
    interval: int

    def __init__(self, *, domain: str, interval: int):
        """
        Initialize the consumer with a domain and polling interval.

        :param domain: ForestMQ server domain, e.g., "http://localhost:8005".
        :param interval: Time in seconds between polling attempts.
        """
        self.domain = domain
        self.interval = interval

    @staticmethod
    def set_headers() -> dict:
        """
        Set HTTP headers for the polling request.

        :return: Dictionary with Content-Type header.
        """
        return {"Content-Type": "application/json"}

    async def poll(self, callback: Callable[[dict], None]) -> None:
        """
        Begin polling the ForestMQ server and invoke the callback with each message.

        Example usage:

            import asyncio
            from forestmq import ForestMQ

            def callback(message: dict) -> None:
                print(f"Consumer message: {message['message']}")

            if __name__ == "__main__":
                fmq = ForestMQ(domain="http://localhost:8005", interval=1)
                asyncio.run(fmq.consumer.poll(callback))

        :param callback: A function that takes a `dict` message and returns `None`.
        :raises ConsumerError: If the HTTP request fails.
        """
        logger.info(f"[ForestMQ Consumer]: Starting polling to {self._get_url()}")
        while True:
            try:
                message = await self._fetch()
                if "error" not in message:
                    callback(message)
            except httpx.RequestError as e:
                raise ConsumerError() from e
            await asyncio.sleep(self.interval)

    async def _fetch(self) -> dict:
        """
        Internal method to send a POST request to the consumer endpoint.

        :return: Decoded JSON response as a dictionary.
        """
        async with httpx.AsyncClient() as client:
            headers = Consumer.set_headers()
            r = await client.post(self._get_url(), headers=headers)
            return r.json()

    def _get_url(self):
        """
        Construct the full consumer polling URL.

        :return: URL string like "http://localhost:8005/consumer".
        """
        return f"{self.domain}/consumer"
