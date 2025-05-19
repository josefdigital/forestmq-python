"""

"""
from forestmq.provider import Provider, Protocol


class ForestMQ:

    domain: str

    provider: Provider

    def __init__(self, *, domain: str):
        self.domain = domain
        tcp = Protocol.TCP
        self.provider = Provider(protocol=tcp, domain=self.domain)
