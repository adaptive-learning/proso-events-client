from .context import event_client
from .test_integration import initialize
from .helpers import *
import pytest


@pytest.mark.skipif(not api_endpoint_available(), reason="requires running API")
def test_performance_insert(tmpdir, delete_table: bool = False):
    db_path = str(tmpdir.join("events.log").realpath())

    event_api, event_logger = initialize(db_path)

    # create test event type

    type_name = 'test_performance'

    event_api.delete_type(type_name)
    event_api.create_type(get_answer_schema(type_name))

    # add events
    for i in range(1000):
        event_logger.emit(type_name, get_answer_random_payload(), ['test'])

    # send to datastore via API
    pusher = event_client.Pusher(event_api, event_logger.event_file, 1000)
    pusher.push_all()

    # delete temporal type

    if delete_table:
        event_api.delete_type(type_name)
