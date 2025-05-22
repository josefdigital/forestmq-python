import asyncio

from forestmq import ForestMQ


async def callback(message: dict) -> None:
    await asyncio.sleep(1)
    print(f"Consumer message: {message['message']}")


if __name__ == "__main__":
    fmq = ForestMQ(domain="http://localhost:8005", interval=1)
    asyncio.run(fmq.consumer.poll(callback))
