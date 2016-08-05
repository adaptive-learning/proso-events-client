# -*- coding: utf-8 -*-

import simplejson as json
import requests
import hashlib
import psycopg2
import datetime


class EventClient:
    def __init__(self, token, endpoint, source='default'):
        self.source = source
        self.endpoint = endpoint
        self.token = token

    def get_headers(self) -> dict:
        return {
            'x-api-token': self.token,
        }

    def push_event(self, event_type: str, data: dict):
        return self.push_many_events(event_type, [data])

    def push_many_events(self, event_type: str, data: list):
        for i in range(len(data)):
            data[i]['source'] = self.source

        return self.api_post_req('/type/%s/event' % event_type, data)

    def create_type(self, json_schema):
        self.api_post_req('/type', json_schema)

    def api_post_req(self, path, data):
        data = json.dumps(data)

        req = requests.post(self.endpoint + path, headers=self.get_headers(), data=data)
        if req.status_code != 201:
            raise Exception("Event storage error. Status: %s" % req.status_code)

    def get_types(self):
        req = requests.get("%s/type" % self.endpoint, headers=self.get_headers())
        return req.json()

    def delete_type(self, type_name):
        req = requests.delete("%s/type/%s" % (self.endpoint, type_name), headers=self.get_headers())

        if req.status_code != 200:
            raise Exception("Event storage error. Status: %s" % req.status_code)

    def get_db_connection(self):
        req = requests.get("%s/db" % self.endpoint, headers=self.get_headers())

        if req.status_code != 200:
            raise Exception("Event storage error. Status: %s" % req.status_code)

        return psycopg2.connect(**req.json())
