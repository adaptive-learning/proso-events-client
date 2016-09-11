from .context import event_client
from .helpers import *


def test_file_logging(tmpdir):
    db_path = str(tmpdir.join("event.log").realpath())
    ev = event_client.EventsLogger(db_path, 'test')

    payload = get_payload()

    for p in payload:
        ev.emit('test_answer', p)

    assert all([event in payload for event in ev.event_file.read_events()])
