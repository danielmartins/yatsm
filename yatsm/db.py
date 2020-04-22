import json

from walrus import Database

db = Database(host="localhost", port=6379, db=0)


def serialize(data):
    return json.dumps(data)


def deserialize(data):
    return json.loads(data)
