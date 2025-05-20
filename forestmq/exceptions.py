class ForestMQError(Exception):
    """
    Base exception class for all ForestMQ-related errors.

    All other custom exceptions inherit from this.
    """
    pass


class ConsumerError(ForestMQError):
    """
    Raised when a consumer encounters an error during message polling
    or handling.

    :raises ConsumerError: if a message cannot be consumed or an internal
                           failure occurs within the consumer.
    """
    pass


class ProviderError(ForestMQError):
    """
    Raised when the provider fails to send a message or is misconfigured.

    :raises ProviderError: if message delivery or provider setup fails.
    """
    pass


class SessionError(ForestMQError):
    """
    Raised when an HTTP session or request fails during communication
    with the ForestMQ server.

    :raises SessionError: if there is a transport-level failure in sending
                          or receiving data via HTTP/HTTPS.
    """
    pass
