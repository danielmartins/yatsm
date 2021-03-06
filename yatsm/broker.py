import os

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.brokers.stub import StubBroker

from yatsm.settings import settings

if os.getenv("UNIT_TESTS") == "1":
    broker = StubBroker()
    broker.emit_after("process_boot")
else:
    broker = RedisBroker(url=str(settings.redis_dsn))
    # result_backend = RedisBackend()
    # broker.add_middleware(Results(backend=result_backend))
    dramatiq.set_broker(broker)
