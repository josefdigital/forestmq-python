# ForestMQ Python

Python client for [ForestMQ](https://github.com/josefdigital/forestmq)


### Install
```
pip install forestmq
```

### Running ForestMQ
```
docker run -p 8005:8005 josefdigital/forestmq:0.6.2
```

### Examples
#### Using the provider API
```python
from forestmq import ForestMQ


def sync_example():
    fmq = ForestMQ(domain="http://localhost:8005")
    result = fmq.provider.send_msg_sync({
        "name": "Sync message",
    })
    print(result)

sync_example()  # {'queue_length': 38, 'message_size': 5120, 'message': {'name': 'Sync message'}}
```

Using the provider's async client
```python
import asyncio
from forestmq import ForestMQ

async def async_example():
    fmq = ForestMQ(domain="http://localhost:8005")
    result = await fmq.provider.send_msg({
        "name": "Async message!",
    })
    print(result)

asyncio.run(async_example())  # {'queue_length': 39, 'message_size': 5120, 'message': {'name': 'Async message!'}}
```
#### Using the consumer API
```python
import asyncio

from forestmq import ForestMQ


def callback(message: dict) -> None:
    print(f"Consumer message: {message['message']}")


if __name__ == "__main__":
    fmq = ForestMQ(domain="http://localhost:8005", interval=1)
    asyncio.run(fmq.consumer.poll(callback))

```


