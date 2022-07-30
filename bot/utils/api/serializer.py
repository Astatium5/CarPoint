import json


def serialize_content(content: bytes) -> dict:
    return json.loads(content)
