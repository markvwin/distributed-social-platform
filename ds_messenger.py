"""
Mark Nguyen
84257566
markvn@uci.edu
"""

import json
import time
import ds_client
import ds_protocol
import Profile


class DirectMessage:
    """Class that creates DirectMessage object"""
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """Class that sends and retrieves direct message objects"""
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.usr = username
        self.pwd = password

    def check_response(self):
        """method that checks for a server response by requesting token"""
        resp = ds_client.basic_send(self.dsuserver, 3021, self.usr, self.pwd,
                                    token=True)
        if resp:
            return resp
        if not resp:
            return False  # Returns False if there is connection error.

    def get_token(self):
        """method that retrieves token from server"""
        resp = ds_client.basic_send(self.dsuserver, 3021, self.usr, self.pwd,
                                    token=True)
        if resp:
            if resp.type == 'error':
                return False
            if resp.type == 'ok':
                return resp.token
        if not resp:
            return False

    def send(self, message: str, recipient: str) -> bool:
        """method that sends direct messages"""
        # must return true if message successfully sent, false if send failed.
        self.token = self.get_token()
        if not self.token:
            return False
        timestamp = time.time()
        request = {"token": self.token,
                   "directmessage": {"entry": message, "recipient": recipient,
                                     "timestamp": timestamp}}
        request = json.dumps(request)
        ds_client.basic_send(self.dsuserver, 3021, self.usr, self.pwd,
                             request=request)
        if Profile.LOGGED_IN:
            temp = DirectMessage()
            temp.recipient = recipient
            temp.message = message
            temp.timestamp = timestamp
            temp_profile = Profile.Profile()
            temp_profile.load_profile(Profile.PROFILE_DIRECTORY)
            temp_profile.my_messages.append(temp.__dict__)
            if recipient not in temp_profile.friends:
                temp_profile.friends.append(recipient)
            temp_profile.save_profile(Profile.PROFILE_DIRECTORY)
            print('sent')
        return True

    def retrieve_new(self) -> list:
        """method that retrieve new messages sent to the profile"""
        # must return a list of DirectMessage objects containing all new
        # messages
        self.token = self.get_token()
        if self.token:
            request = {"token": self.token, "directmessage": 'new'}
            request = json.dumps(request)
            resp = ds_client.basic_send(self.dsuserver, 3021, self.usr,
                                        self.pwd, request=request)
            resp = ds_protocol.extract_json_dms(resp)
            if resp.type == 'ok':
                messages_dict = ds_protocol.extract_messages(resp.messages)
                dm_list = []
                for key in messages_dict.keys():
                    msgs_from_user_list = messages_dict[key]
                    for value in msgs_from_user_list:
                        msg_tuple = value
                        temp = DirectMessage()
                        temp.recipient = key
                        temp.message = msg_tuple[0]
                        temp.timestamp = msg_tuple[1]
                        dm_list.append(temp)
                if Profile.LOGGED_IN:
                    temp_profile = Profile.Profile()
                    temp_profile.load_profile(Profile.PROFILE_DIRECTORY)
                    for item in dm_list:
                        if item.recipient not in temp_profile.friends:
                            temp_profile.friends.append(item.recipient)
                        temp_profile.messages.append(item.__dict__)
                    temp_profile.save_profile(Profile.PROFILE_DIRECTORY)
                return dm_list

    def retrieve_all(self) -> list:
        """method that retrieve all messages sent to the profile"""
        # must return a list of DirectMessage objects containing all messages
        self.token = self.get_token()
        if self.token:
            request = {"token": self.token, "directmessage": 'all'}
            request = json.dumps(request)
            resp = ds_client.basic_send(self.dsuserver, 3021, self.usr,
                                        self.pwd, request=request)
            resp = ds_protocol.extract_json_dms(resp)
            if resp.type == 'ok':
                messages_dict = ds_protocol.extract_messages(resp.messages)
                dm_list = []
                serialized_dm_list = []
                for key in messages_dict.keys():
                    msgs_from_user_list = messages_dict[key]
                    for value in msgs_from_user_list:
                        msg_tuple = value
                        temp = DirectMessage()
                        temp.recipient = key
                        temp.message = msg_tuple[0]
                        temp.timestamp = msg_tuple[1]
                        dm_list.append(temp)
                        serialized_dm_list.append(temp.__dict__)
                if Profile.LOGGED_IN:
                    temp_profile = Profile.Profile()
                    temp_profile.load_profile(Profile.PROFILE_DIRECTORY)
                    temp_profile.messages.extend(serialized_dm_list)
                    removing_dupes = []
                    dupes_removed = []
                    for item in temp_profile.messages:
                        removing_dupes.append(json.dumps(item))
                    removing_dupes = list(set(removing_dupes))
                    for item in removing_dupes:
                        dupes_removed.append(json.loads(item))
                    temp_profile.messages = dupes_removed

                    for item in dm_list:
                        if item.recipient not in temp_profile.friends:
                            temp_profile.friends.append(item.recipient)
                    temp_profile.save_profile(Profile.PROFILE_DIRECTORY)
                return dm_list
#
#
# if __name__ == "__main__":
#     x = DirectMessenger("168.235.86.101", 'SukmaD', "123456789")
#     print(x.send('hi', 'SukmaD'))
#     print(x.retrieve_all())
