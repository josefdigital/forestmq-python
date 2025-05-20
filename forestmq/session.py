from urllib.parse import urljoin
import json

import httpx

from forestmq.logger import logger


class Session:
    """
     Session class for handling synchronous and asynchronous HTTP communication
     with a ForestMQ server.

     This class wraps `httpx` to send messages to a configured ForestMQ endpoint.

     Example usage:

         from forestmq.session import Session

         session = Session(domain="http://localhost:8005", path="/provider")
         response = session.send_msg_sync(message={"key": "value"})
         print(response.status_code)
     """
    domain: str
    path: str
    url: str
    headers: dict
    client: httpx.Client

    def __init__(self, *, domain: str, path: str):
        """
        Initialize the Session instance.

        :param domain: The base URL of the ForestMQ server (e.g., "http://localhost:8005").
        :param path: The endpoint path to send messages to (e.g., "/provider").
        """
        self.domain = domain
        self.path = path
        self.client = httpx.Client()
        self.headers = {
            "Content-Type": "application/json",
        }
        self.url = urljoin(self.domain, self.path)

    def send_msg_sync(self, *, message: dict) -> httpx.Response:
        """
        Send a message synchronously to the ForestMQ server.

        :param message: The message dictionary to send as JSON.
        :return: The response from the ForestMQ server.

        Example:

            session = Session(domain="http://localhost:8005", path="/provider")
            response = session.send_msg_sync(message={"name": "Sync message"})
            print(response.json())
        """
        response = self.client.post(
            url=self.url,
            json=message,
            headers=self.headers,
        )
        response.raise_for_status()
        return response

    async def send_msg(self, *, message: dict) -> httpx.Response:
        """
        Send a message asynchronously to the ForestMQ server.

        :param message: The message dictionary to send as JSON.
        :return: The async response from the ForestMQ server.

        Example:

            import asyncio

            async def main():
                session = Session(domain="http://localhost:8005", path="/provider")
                response = await session.send_msg(message={"name": "Async message!"})
                print(response.json())

            asyncio.run(main())
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=self.url,
                json=message,
            )
            response.raise_for_status()
            return response

    def close(self):
        """
        Close the internal httpx.Client.

        :return: None
        """
        self.client.close()
