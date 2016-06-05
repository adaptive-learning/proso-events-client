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


def test_sqlite_logging(tmpdir):
    db_path = str(tmpdir.join("example.db").realpath())
    ev = event_client.EventsLogger(db_path, 'test')

    payload = get_payload()

    for p in payload:
        ev.emit('test_answer', p)

    assert all([(e.payload in payload) for e in ev.read_all()])
    ev.emit('test_answer', {'payload': 'test'})
    assert all([(e.payload in payload) for e in ev.read_all()]) is False


def test_sqlite_ack_event(tmpdir):
    db_path = str(tmpdir.join("example.db").realpath())
    ev = event_client.EventsLogger(db_path, 'test')

    for p in get_payload(10):
        ev.emit('test_answer', p)

    for e in ev.read_new():
        e.set_ack()
        break

    assert len(list(ev.read_new())) == 9 and len(list(ev.read_all())) == 10


