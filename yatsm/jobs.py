import dramatiq

from yatsm.broker import broker as redis_broker
from yatsm.db import db, serialize


@dramatiq.actor(queue_name="default", broker=redis_broker)
def success(message_data, result):
    print(f"The result of message {message_data['message_id']} was {result}.")
    data = db.Hash(message_data["options"]["message_id"])
    data.update(result=serialize(result), message_data=serialize(message_data))


@dramatiq.actor(queue_name="default", broker=redis_broker)
def failure(message_data, exception_data):
    print(f"Message {message_data['message_id']} failed:")
    print(f"  * type: {exception_data['type']}")
    print(f"  * message: {exception_data['message']!r}")
    data = db.Hash(message_data["options"]["message_id"])
    data.update(
        message_data=serialize(message_data), exception_data=serialize(exception_data)
    )


@dramatiq.actor(queue_name="default", broker=redis_broker)
def heavy_job(url: str = "google.comr"):
    print("Heavy job")
    print("Finished job")
    return url


@dramatiq.actor(queue_name="default", broker=redis_broker)
def heavy_job_with_fail():
    print("Heavy job")
    raise ValueError("Deu ruim")
