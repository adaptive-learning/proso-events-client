from .context import event_client
from .test_file_log import get_payload
from .test_integration import api_endpoint_available, initialize
import pytest


@pytest.mark.skipif(not api_endpoint_available(), reason="requires running API")
def test_performance_insert(tmpdir, delete_table: bool = False):
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

    for i in range(10):
        payload = get_payload(100)

        for i in payload:
            event_logger.emit(type_name, i, ['test'])

    # send to datastore via API
    event_client.Pusher.push_all(event_api, event_logger.event_file)

    # retrieve events

    conn = event_api.get_db_connection()
    cursor = conn.cursor()

    # event_api.get_events(type_name, 'test', [], datetime.datetime.now() - datetime.timedelta(days=1), datetime.datetime.now())

    # delete temporal type

    if delete_table:
        event_api.delete_type(type_name)
