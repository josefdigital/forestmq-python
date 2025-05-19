from urllib.parse import urljoin
import json

import httpx

from forestmq.logger import logger


class Session:

    domain: str
    path: str
    url: str
    headers: dict
    client: httpx.Client

    def __init__(self, *, domain: str, path: str):
        self.domain = domain
        self.path = path
        self.client = httpx.Client()
        self.headers = {
            "Content-Type": "application/json",
        }
        self.url = urljoin(self.domain, self.path)

    def send_msg_sync(self, *, message: dict) -> httpx.Response:
        response = self.client.post(
            url=self.url,
            json=message,
            headers=self.headers,
        )
        response.raise_for_status()
        return response

    async def send_msg(self, *, message: dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=self.url,
                json=message,
            )
            response.raise_for_status()
            return response

    def close(self):
        self.client.close()
