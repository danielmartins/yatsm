import birdisle.redis
import dramatiq
import pytest
from dramatiq import Worker
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from starlette.testclient import TestClient

from yatsm.broker import broker


@pytest.fixture
def server():
    server = birdisle.Server()
    yield server
    server.close()


@pytest.fixture
def r(server):
    redis = birdisle.redis.StrictRedis(server=server)
    yield redis


@pytest.fixture()
def redis_broker(r):
    broker = RedisBroker()
    broker.client = r
    broker.client.flushall()
    result_backend = RedisBackend()
    result_backend.client = r
    broker.add_middleware(Results(backend=result_backend))
    broker.emit_after("process_boot")
    # monkeypatch.setattr("yatsm.jobs.redis_broker", broker)
    dramatiq.set_broker(broker)
    yield broker
    broker.client.flushall()
    broker.close()


@pytest.fixture
def request_client(redis_broker):
    from yatsm.main import app

    client = TestClient(app)
    return client


@pytest.fixture()
def stub_broker(r):
    result_backend = RedisBackend()
    result_backend.client = r
    broker.add_middleware(Results(backend=result_backend))
    broker.flush_all()
    dramatiq.set_broker(stub_broker)
    return broker


@pytest.fixture()
def stub_worker():
    worker = Worker(broker, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()
