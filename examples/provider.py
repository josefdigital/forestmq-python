import asyncio

from forestmq import ForestMQ


def sync_example():
    fmq = ForestMQ(domain="http://localhost:8005")
    result = fmq.provider.send_msg_sync({
        "name": "Sync message",
    })
    print(result)


async def async_example():
    fmq = ForestMQ(domain="http://localhost:8005")
    result = await fmq.provider.send_msg({
        "name": "Async message!",
    })
    print(result)


if __name__ == "__main__":
    sync_example()
    asyncio.run(async_example())
