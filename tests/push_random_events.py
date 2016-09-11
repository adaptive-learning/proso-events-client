import uuid
import os
import progressbar
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

import proso.events.client as event_client
from helpers import *

if __name__ == '__main__':
    event_number = int(sys.argv[1])

    db_path = '/tmp/%s.log' % str(uuid.uuid4())
    event_api, event_logger = event_client.EventClient(os.environ['proso_events_token'], os.environ['proso_events_url'], 'test'), event_client.EventsLogger(db_path, 'test')

    # create test event type

    type_name = 'test_performance'

    event_api.delete_type(type_name)
    event_api.create_type(get_answer_schema(type_name))

    # add events
    bar = progressbar.ProgressBar()
    pusher = event_client.Pusher(event_api, event_logger.event_file, 1500)

    for i in bar(range(event_number)):
        event_logger.emit(type_name, get_answer_random_payload(), ['test'])

        if i % 1000 == 0: pusher.push_all()

    # send to datastore via API
    pusher.push_all()

    # remove temp file
    os.remove(db_path)
