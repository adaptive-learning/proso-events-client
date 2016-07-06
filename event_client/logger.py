import json
import datetime
import zlib
import base64


class EventsLogger:
    def __init__(self, log_path: str, source: str):
        self.event_file = EventFile(log_path)
        self.source = source

    def emit(self, event_type: str, data: dict, tags: list = [], time: datetime.datetime = datetime.datetime.now()):
        """
        Add new event to datastore (file).
        """

        data['_type'] = event_type
        data['tags'] = tags
        data['datetime'] = str(time)
        data['source'] = str(self.source)

        self.event_file.write(data)


class EventFile:
    def __init__(self, log_path: str):
        self.log_path = log_path

    def write(self, data: dict):
        """
        Write dict to file (JSON + CRC)
        """
        data = json.dumps(data)
        with open(self.log_path, 'a') as f:
            f.write("%s %s\n" % (data, zlib.crc32(data.encode())))
            f.flush()

    def read_events(self):
        """
        Read events from file and validate CRC.
        Damaged records are skipped.
        """
        with open(self.log_path, 'r') as f:
            for line in f:
                last_space = line.rfind(' ')
                if int(line[last_space + 1:-1]) == zlib.crc32(line[:last_space].encode()):
                    yield json.loads(line[:last_space])
                else:
                    pass  # skip damaged records
