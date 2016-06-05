from . import *


class Pusher:
    @staticmethod
    def push_all_new(api_client: EventClient, event_logger: EventsLogger):
        for event in event_logger.read_new():
            api_client.push_event(event.event_type, event.payload)
            event.set_ack()
