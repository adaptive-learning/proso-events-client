from .context import event_client
import pytest
from .helpers import *
import datetime
import random


def initialize(db_path):
    return event_client.EventClient(os.environ['proso_events_token'], os.environ['proso_events_url'], 'test'), event_client.EventsLogger(db_path, 'test')


@pytest.mark.skipif(not api_endpoint_available(), reason="requires running API")
def test_integration(tmpdir, delete_table: bool = True):
    db_path = str(tmpdir.join("events.log").realpath())

    event_api, event_logger = initialize(db_path)

    # create test event type

    type_name = 'test_answer'

    event_api.delete_type(type_name)
    event_api.create_type(get_answer_schema(type_name))

    # add events
    payload = get_payload(10)
    for i in payload:
        event_logger.emit(type_name, i, ['test'], datetime.datetime.fromtimestamp(random.randint(1325376000, 1476298681)))

    # send to datastore via API
    pusher = event_client.Pusher(event_api, event_logger.event_file)
    pusher.push_all()

    # retrieve events

    conn = event_api.get_db_connection()
    cursor = conn.cursor()

    # event_api.get_events(type_name, 'test', [], datetime.datetime.now() - datetime.timedelta(days=1), datetime.datetime.now())

    # delete temporal type

    if delete_table:
        event_api.delete_type(type_name)
