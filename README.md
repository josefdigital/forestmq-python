# 🌲 ForestMQ Python Client

**ForestMQ Python** is the official client library for [ForestMQ](https://github.com/josefdigital/forestmq), a lightweight, fast, and embeddable in-memory message queue.

📘 [Read the Docs](https://forestmq-python.readthedocs.io/en/latest/)

---

## 📦 Installation

```bash
pip install forestmq
```

---

## 🚀 Running ForestMQ Locally

```bash
docker run -p 8005:8005 josefdigital/forestmq:0.6.2
```

---

## 💬 Examples

### ✅ Provider API (Synchronous)

```python
from forestmq import ForestMQ

def sync_example():
    fmq = ForestMQ(domain="http://localhost:8005")
    result = fmq.provider.send_msg_sync({
        "name": "Sync message",
    })
    print(result)

sync_example()
# Output: {'queue_length': 38, 'message_size': 5120, 'message': {'name': 'Sync message'}}
```

---

### ✅ Provider API (Asynchronous)

```python
import asyncio
from forestmq import ForestMQ

async def async_example():
    fmq = ForestMQ(domain="http://localhost:8005")
    result = await fmq.provider.send_msg({
        "name": "Async message!",
    })
    print(result)

asyncio.run(async_example())
# Output: {'queue_length': 39, 'message_size': 5120, 'message': {'name': 'Async message!'}}
```

---

### 📥 Consumer API (Synchronous Callback)

```python
import asyncio
from forestmq import ForestMQ

def callback(message: dict) -> None:
    print(f"Consumer message: {message['message']}")

if __name__ == "__main__":
    fmq = ForestMQ(domain="http://localhost:8005", interval=1)
    asyncio.run(fmq.consumer.poll_sync(callback))
```

---

### 📥 Consumer API (Async Callback)

```python
import asyncio
from forestmq import ForestMQ

async def callback(message: dict) -> None:
    await asyncio.sleep(1)
    print(f"Consumer message: {message['message']}")

if __name__ == "__main__":
    fmq = ForestMQ(domain="http://localhost:8005", interval=1)
    asyncio.run(fmq.consumer.poll(callback))
```

---

## 🛠️ Features

- Lightweight async-first client
- Built-in support for both sync and async providers
- Polling consumer with coroutine support
- Built-in retries, logging, and extensibility