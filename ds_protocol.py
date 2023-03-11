# Mark Nguyen
# markvn@uci.edu
# 84257566

import json
from collections import namedtuple

""" Namedtuple to hold the values retrieved from json messages. """
DataTuple = namedtuple('TokenTuple', ['type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
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
            return DataTuple(resp_type, message, token)
        else:
            return DataTuple(resp_type, message, '')
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
