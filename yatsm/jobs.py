import dramatiq

from yatsm.broker import broker as redis_broker
from yatsm.db import db, deserialize, serialize


@dramatiq.actor(queue_name="default", broker=redis_broker)
def success(message_data, result):
    print(f"The result of message {message_data['message_id']} was {result}.")
    data = db.Hash(message_data["options"]["message_id"])
    if "results" not in data:
        r = []
    else:
        r = deserialize(data["results"])
    r.append({"message_data": message_data, "result": result})
    data.update(results=serialize(r))


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
def fibonacci(nterms: int):
    # first two terms
    n1, n2 = 0, 1
    count = 0
    t = []

    # check if the number of terms is valid
    if nterms <= 0:
        ValueError("Need a positive integer")
    elif nterms == 1:
        t.append(n1)
    else:
        print("Fibonacci sequence:")
        while count < nterms:
            t.append(n1)
            # print(n1)
            nth = n1 + n2
            # update values
            n1 = n2
            n2 = nth
            count += 1
    return t


@dramatiq.actor(queue_name="default", broker=redis_broker)
def heavy_job(url: str = "google.comr"):
    print("Heavy job")
    print("Finished job")
    return url


@dramatiq.actor(queue_name="default", broker=redis_broker)
def heavy_job_with_fail():
    print("Heavy job")
    raise ValueError("Deu ruim")
