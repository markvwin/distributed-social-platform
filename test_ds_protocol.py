"""
Mark Nguyen
markvn@uci.edu
84257566
"""

import ds_protocol
import json


def test_extract_json():
    response = {"response": {"type": "ok", "message": "",
                             "token": "12345678-1234-1234-1234-123456789abc"}}
    response = json.dumps(response)
    extracted_response = ds_protocol.extract_json(response)
    assert extracted_response.type == 'ok'
    assert extracted_response.message == ""
    assert extracted_response.token == "12345678-1234-1234-1234-123456789abc"


def test_extract_json_dms():
    response = {"response": {"type": "ok", "messages": [
        {"message": "Hello User 1!", "from": "markb",
         "timestamp": "1603167689.3928561"}]}}
    response = json.dumps(response)
    extract_response = ds_protocol.extract_json_dms(response)
    assert extract_response.type == 'ok'
    assert extract_response.messages == [
        {"message": "Hello User 1!", "from": "markb",
         "timestamp": "1603167689.3928561"}]


def test_json_decode_error():
    response = "jello"
    extracted_response = ds_protocol.extract_json(response)
    extracted_response1 = ds_protocol.extract_json_dms(response)
