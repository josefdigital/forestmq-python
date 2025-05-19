class ForestMQError(Exception):
    pass


class ProviderError(ForestMQError):
    pass


class SessionError(ForestMQError):
    pass
