from .context import event_client
from .test_file_log import get_payload
import pytest
import os


def api_endpoint_available():
    return not all([i in os.environ for i in ['events_client_id', 'events_client_secret', 'events_client_url']])


def initialize(db_path):
    return event_client.EventClient(os.environ['events_client_id'], os.environ['events_client_secret'], os.environ['events_client_url'], 'test'), event_client.EventsLogger(db_path, 'test')


@pytest.mark.skipif(api_endpoint_available(), reason="requires running API")
def test_function(tmpdir):
    db_path = str(tmpdir.join("example.db").realpath())

    event_api, event_logger = initialize(db_path)

    # create test event type

    try:
        event_api.create_type({
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
    except:
        pass

    # add events
    payload = get_payload(10)

    for i in payload:
        event_logger.emit('answer_test', i, ['test'])

        # send to datastore via API

    event_client.Pusher.push_all_new(event_api, event_logger)
