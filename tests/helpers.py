import random
import os


def api_endpoint_available():
    return all([i in os.environ for i in ['proso_events_token', 'proso_events_url']])


def get_answer_schema(type_name: str):
    return {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": type_name,
        "description": "answer event",
        "type": "object",
        "properties": {
            "user_id": {
                "description": "The unique identifier for the user.",
                "type": "integer"
            },
            "is_correct": {
                "type": "boolean"
            },
            "context_id": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            },
            "item_id": {
                "type": "integer"
            },
            "response_time_ms": {
                "description": "User's response time in miliseconds.",
                "type": "integer"
            },
            "params": {
                "type": "object"
            }
        },
        "required": ["user_id", "is_correct", "context_id", "item_id"]
    }


def get_answer_random_payload():
    return {
        "user_id": random.randint(1, 100),
        "is_correct": True if random.random() > 0.2 else False,
        "context_id": [random.randint(1, 30000) for i in range(random.randint(0, 5))],
        "item_id": random.randint(1, 50000),
        "response_time_ms": random.randint(950, 20000),
        "params": {
            "system": random.choice(["slepemapy.cz", "devel.slepemapy.cz", "anatom.cz", "umimecesky.cz"])
        }}


def get_payload(n: int = 10) -> list:
    return [get_answer_random_payload() for i in range(n)]
