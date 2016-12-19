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

    event_api.meta_set('test', 'item_id', str(2344), 'bbla bla bla')
