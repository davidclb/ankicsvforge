import json
import urllib.request
import logging

DEFAULT_URL = 'http://127.0.0.1:8765'


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    logging.debug(f"la requete json {requestJson}")
    response = json.load(urllib.request.urlopen(urllib.request.Request(DEFAULT_URL, requestJson), timeout=5))
    logging.debug(f"la reponse {response}")
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']
