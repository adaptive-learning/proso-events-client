from event_client import *
import sys
import random
import string
import progressbar


def random_string(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


if __name__ == '__main__':
    api_id, api_secret = sys.argv[1:3]

    client = EventClient(api_id, api_secret)

    client.create_type({
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "answer_test",
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
                "type": "integer"
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
    })

    bar = progressbar.ProgressBar()
    for i in bar(range(10 ** 3)):
        client.push_event('answer_test', {
            "user_id": random.randint(1, 100),
            "is_correct": True if random.random() > 0.2 else False,
            "context_id": random.randint(1, 100),
            "item_id": random.randint(1, 50000),
            "response_time_ms": random.randint(950, 20000),
            "params": {
                "system": random.choice(["slepemapy.cz", "devel.slepemapy.cz", "anatom.cz", "umimecesky.cz"])
            }
        })
