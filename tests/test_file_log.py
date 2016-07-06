from .context import event_client
import random


def get_payload(n: int = 10) -> list:
    res = []
    for i in range(n):
        res.append({
            "user_id": random.randint(1, 100),
            "is_correct": True if random.random() > 0.2 else False,
            "context_id": random.randint(1, 100),
            "item_id": random.randint(1, 50000),
            "response_time_ms": random.randint(950, 20000),
            "params": {
                "system": random.choice(["slepemapy.cz", "devel.slepemapy.cz", "anatom.cz", "umimecesky.cz"])
            }})

    return res


def test_file_logging(tmpdir):
    db_path = str(tmpdir.join("event.log").realpath())
    ev = event_client.EventsLogger(db_path, 'test')

    payload = get_payload()

    for p in payload:
        ev.emit('test_answer', p)

    assert all([event in payload for event in ev.event_file.read_events()])
