import json

from walrus import Database

from yatsm.settings import settings

db = Database(
    host=settings.redis_dsn.host,
    port=settings.redis_dsn.port,
    db=settings.redis_dsn.path[-1],
)


def serialize(data):
    return json.dumps(data)


def deserialize(data):
    return json.loads(data)
