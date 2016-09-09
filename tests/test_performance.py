from .context import event_client
from .test_file_log import get_payload
from .test_integration import api_endpoint_available, initialize
import pytest


@pytest.mark.skipif(not api_endpoint_available(), reason="requires running API")
def test_performance_insert_1000(tmpdir, delete_table: bool = False):
    db_path = str(tmpdir.join("events.log").realpath())

    event_api, event_logger = initialize(db_path)

    # create test event type

    type_name = 'test_performance'

    event_api.delete_type(type_name)

    event_api.create_type({
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

    # add events

    payload = get_payload(1000)

    for i in payload:
        event_logger.emit(type_name, i, ['test'])

    # send to datastore via API
    pusher = event_client.Pusher(event_api, event_logger.event_file)
    pusher.push_all()

    # delete temporal type

    if delete_table:
        event_api.delete_type(type_name)
