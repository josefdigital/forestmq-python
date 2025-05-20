"""

"""
from forestmq.provider import Provider, Protocol
from forestmq.consumer import Consumer


class ForestMQ:

    domain: str
    interval: int
    provider: Provider
    consumer: Consumer

    def __init__(self, *, domain: str, interval: int = 1):
        self.domain = domain
        self.interval = interval
        tcp = Protocol.TCP
        self.provider = Provider(protocol=tcp, domain=self.domain)
        self.consumer = Consumer(domain=self.domain, interval=self.interval)
