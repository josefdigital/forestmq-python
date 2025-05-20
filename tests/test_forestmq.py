import pytest
import httpx
from unittest.mock import AsyncMock, patch

from forestmq import ForestMQ
from forestmq.exceptions import SessionError


@pytest.fixture
def fmq():
    return ForestMQ(domain="http://localhost:8005")


def test_send_msg_sync(monkeypatch, fmq):
    """Test provider.send_msg_sync() returns expected data"""

    class MockResponse:
        status_code = 200

        def json(self):
            return {
                "queue_length": 1,
                "message_size": 64,
                "message": {"name": "Sync message"},
            }

        def raise_for_status(self):
            pass  # Simulates no HTTP error

    import httpx
    monkeypatch.setattr(httpx.Client, "post", lambda self, *a, **k: MockResponse())

    result = fmq.provider.send_msg_sync({"name": "Sync message"})
    assert result["message"]["name"] == "Sync message"


@pytest.mark.asyncio
async def test_send_msg_async():
    """Test forestmq.provider.send_msg() returns expected coroutine with correct JSON data."""

    expected_json = {
        "queue_length": 1,
        "message_size": 64,
        "message": {"name": "Async message"},
    }

    # Mock response object
    mock_response = AsyncMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json = AsyncMock(return_value=expected_json)

    # Mock client context
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client

    with patch("httpx.AsyncClient", return_value=mock_client):
        fmq = ForestMQ(domain="http://localhost:8005")

        # This returns a coroutine (resp.json()), so we await it
        json_coro = await fmq.provider.send_msg({"name": "Async message"})
        result = await json_coro  # Await the coroutine returned by send_msg

        assert result["message"]["name"] == "Async message"
        assert result["queue_length"] == 1


@pytest.mark.asyncio
async def test_send_msg_async_failure():
    """Test provider.send_msg() raises SessionError on request failure."""

    # Simulate a network error
    async def mock_post(*args, **kwargs):
        raise httpx.RequestError("Simulated connection error")

    mock_client = AsyncMock()
    mock_client.post = mock_post
    mock_client.__aenter__.return_value = mock_client

    with patch("httpx.AsyncClient", return_value=mock_client):
        fmq = ForestMQ(domain="http://localhost:8005")

        with pytest.raises(SessionError, match="FORESTMQ Error: Failed to send message in session"):
            coro = await fmq.provider.send_msg({"name": "Failure test"})
            await coro  # This line may not be reached depending on where exception is raised
