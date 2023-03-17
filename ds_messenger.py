"""
Mark Nguyen
84257566
markvn@uci.edu
"""

import ds_client
import ds_protocol
import json
import time
import ui


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.usr = username
        self.pwd = password

    def get_token(self):
        token = ds_client.basic_send(self.dsuserver, 3021, self.usr, self.pwd, token=True)

        return token

    def send(self, message: str, recipient: str) -> bool:
        # must return true if message successfully sent, false if send failed.
        self.token = self.get_token()
        request = {"token": self.token,
                   "directmessage": {"entry": message, "recipient": recipient,
                                     "timestamp": time.time()}}
        request = json.dumps(request)
        resp = ds_client.basic_send(self.dsuserver, 3021, self.usr, self.pwd, request=request)
        if resp:
            resp = ds_protocol.extract_json(resp)
            if resp.type == 'error':
                return False

    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new
        # messages
        self.token = self.get_token()
        request = {"token": self.token, "directmessage": 'new'}
        request = json.dumps(request)
        resp = ds_client.basic_send(self.dsuserver, 3021, self.usr, self.pwd, request=request)
        resp = ds_protocol.extract_json_dms(resp)
        if resp.type == 'ok':
            messages_dict = ds_protocol.extract_messages(resp.messages)
            dm_list = []
            for key, val in messages_dict.items():
                msgs_from_user_list = messages_dict[key]
                for j in range(len(msgs_from_user_list)):
                    msg_tuple = msgs_from_user_list[j]
                    temp = DirectMessage()
                    temp.recipient = key
                    temp.message = msg_tuple[0]
                    temp.timestamp = msg_tuple[1]
                    dm_list.append(temp)
            return dm_list

    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        self.token = self.get_token()
        request = {"token": self.token, "directmessage": 'all'}
        request = json.dumps(request)
        resp = ds_client.basic_send(self.dsuserver, 3021, self.usr, self.pwd,
                                    request=request)
        resp = ds_protocol.extract_json_dms(resp)
        if resp.type == 'ok':
            messages_dict = ds_protocol.extract_messages(resp.messages)
            dm_list = []
            for key, val in messages_dict.items():
                msgs_from_user_list = messages_dict[key]
                for j in range(len(msgs_from_user_list)):
                    msg_tuple = msgs_from_user_list[j]
                    temp = DirectMessage()
                    temp.recipient = key
                    temp.message = msg_tuple[0]
                    temp.timestamp = msg_tuple[1]
                    dm_list.append(temp)
            return dm_list


if __name__ == "__main__":
    x = DirectMessenger("168.235.86.101", 'SukmaD', "123456789")
    x.send('hi', 'SukmaD')
    print(x.retrieve_new())







