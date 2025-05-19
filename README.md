![ForestMQ](assets/fmq_logo.png)
Python client for ForestMQ


## 🚧 Work in progress, please call back soon...

### Install
```
pip install forestmq
```

### Examples
Using the provider
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
