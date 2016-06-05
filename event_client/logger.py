import sqlite3
import json
import datetime


class Event:
    def __init__(self, db: sqlite3.Connection, event_id: int, event_type: str, payload: dict or str, ack: int):
        self.event_type = event_type
        self.db = db
        self.ack = ack
        self.id = event_id
        self.payload = payload

        if type(self.payload) is str:
            self.payload = json.loads(self.payload)

    def set_ack(self, val=1):
        """
        Set event as acknowledged.
        """
        self.db.execute('UPDATE events SET ack = ? WHERE id=?', [val, self.id])
        self.db.commit()


class EventsLogger:
    def __init__(self, log_path: str, source: str):
        self.db = sqlite3.connect(log_path)
        self.source = source

        self.db.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, event_type TEXT NOT NULL, payload TEXT NOT NULL, ack INTEGER NOT NULL DEFAULT 0);')

    def emit(self, event_type: str, data: dict, tags: list = [], time: datetime.datetime = datetime.datetime.now()):
        """
        Add new event to datastore (sqlite).
        """

        data['tags'] = tags
        data['datetime'] = str(time)
        data['source'] = str(self.source)

        self.db.execute('INSERT INTO events(event_type, payload) VALUES (?, ?)', [event_type, json.dumps(data)])
        self.db.commit()

    def read_all(self):
        """
        Read all available events.
        """
        return self._read_wrapper("SELECT * FROM events")

    def read_new(self):
        """
        Read all new (Non-acknowledged) events.
        """
        return self._read_wrapper("SELECT * FROM events WHERE ack = 0")

    def _read_wrapper(self, sql: str) -> iter:
        for row in self.db.execute(sql):
            yield Event(self.db, *row)
