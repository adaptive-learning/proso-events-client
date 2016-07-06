from .client import *
from .logger import *


class Pusher:
    @staticmethod
    def push_all(api_client: EventClient, event_file: EventFile):
        for event in event_file.read_events():
            event_type = event['_type']
            del event['_type']
            api_client.push_event(event_type, event)
