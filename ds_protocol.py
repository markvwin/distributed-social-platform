"""
Mark Nguyen
markvn@uci.edu
84257566
"""

import json
from collections import namedtuple

DATATUPLE = namedtuple('TokenTuple', ['type', 'message', 'token'])
DATATUPLE1 = namedtuple('MessagesTuple', ['type', 'messages'])


def extract_json(json_msg: str):
    """
    Call the json.loads() function on a json string and convert it to a
    DataTuple object
    """
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        resp_type = response['type']
        message = response['message']
        if 'token' in response:
            token = response['token']
            return DATATUPLE(resp_type, message, token)
        return DATATUPLE(resp_type, message, '')
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return


def extract_json_dms(json_msg: str):
    """
    Call the json.loads() function on a json string and convert it to a
    DataTuple object
    """
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        resp_type = response['type']
        messages = response['messages']
        return DATATUPLE1(resp_type, messages)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return


def extract_messages(messages: list) -> dict:
    """
    Message is a list of dictionaries with "message", "from", and
    timestamp" as keys
    """
    msg_dict = {}
    for item in messages:
        user = item['from']
        time = item['timestamp']
        msg = item['message']
        if user in msg_dict:
            msg_dict[user].append((msg, time))
        else:
            msg_dict[user] = [(msg, time)]
    return msg_dict
