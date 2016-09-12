from .context import event_client
import pytest
from .helpers import *
from .test_integration import initialize


@pytest.mark.skipif(not api_endpoint_available(), reason="requires running API")
def test_integration(tmpdir):
    db_path = str(tmpdir.join("events.log").realpath())

    event_api, event_logger = initialize(db_path)

    conn = event_api.get_db_connection()
    cursor = conn.cursor()

    cursor.execute("select * from events_answer limit 10")
    cursor.fetchall()
