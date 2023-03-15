# Mark Nguyen
# markvn@uci.edu
# 84257566

import json
from collections import namedtuple

""" Namedtuple to hold the values retrieved from json messages. """
DATA_TUPLE = namedtuple('TokenTuple', ['type', 'message', 'token'])
DATA_TUPLE1 = namedtuple('MessagesTuple', ['type', 'messages'])


def extract_json(json_msg: str) -> DATA_TUPLE:
    """
    Call the json.loads function on a json string and convert it to a
    DataTuple object
    """
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        resp_type = response['type']
        message = response['message']
        if 'token' in response:
            token = response['token']
            return DATA_TUPLE(resp_type, message, token)
        else:
            return DATA_TUPLE(resp_type, message, '')
    except json.JSONDecodeError:
        print("Json cannot be decoded.")


def extract_json_dms(json_msg: str) -> DATA_TUPLE1:
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        resp_type = response['type']
        messages = response['messages']
        # Message is a list of dictionaries with "message", "from", and
        # "timestamp" as keys
        return DATA_TUPLE1(resp_type, messages)

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
