"""
Mark Nguyen
markvn@uci.edu
84257566
"""

import socket
import json
from types import NoneType
import time

import ui
import ipaddress

import user_interface
from ds_protocol import extract_json


def send(server: str, port: int, username: str, password: str, message: str,
         bio: str = None):
    """Send function sends data to DSU server."""
    if message is None:
        message = ''
    try:
        assert type(server) == str, 'Type server is not a string.'
        assert server
        assert ipaddress.ip_address(server) != ValueError, 'Invalid IP.'
        assert type(port) == int, 'Type port is not a integer.'
        assert 1 <= port <= 65535, 'Port number limit bypassed.'
        assert type(username) == str
        assert username  # checks that username is not empty
        assert ' ' not in username, 'Username cannot contain any whitespace.'
        assert type(password) == str
        assert password  # checks that password is not empty
        assert ' ' not in password, 'Password cannot contain any whitespace.'
        assert type(message) == str or type(message) is None
        if type(message) == str:
            assert not message.isspace(), 'No whitespace in message.'
        assert (type(bio) == str or type(bio) == NoneType)
        assert (bio and message) or (not bio and message) or (
                    bio and (not message or message is None))
        if type(bio) == str:
            assert not bio.isspace(), 'Bio cannot only consist of whitespace.'
    except AssertionError:
        return False

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server, port))
            if not ui.logged_in:
                temp = {"join": {'username': username, 'password': password,
                                 'token': ''}}

                join_msg = json.dumps(temp)
                send1 = sock.makefile('w')
                recv = sock.makefile('r')
                send1.write(join_msg + '\r\n')
                send1.flush()
                resp = recv.readline()
                resp = extract_json(resp)
                if resp.type == 'error':
                    return False

                ui.token = resp.token
                ui.logged_in = True

            if ui.logged_in:
                if message:  # if message is not none
                    message = {'entry': message, 'timestamp': time.time()}
                    temp = {"token": ui.token, "post": message}
                    join_msg = json.dumps(temp)
                    send1 = sock.makefile('w')
                    recv = sock.makefile('r')

                    send1.write(join_msg + '\r\n')
                    send1.flush()

                    resp = recv.readline()
                    resp = extract_json(resp)
                    print(f'\n{resp.message}.')
                    if resp.type == 'error':
                        return False

                if bio:  # if bio is not none
                    bio = {'entry': bio, 'timestamp': time.time()}
                    temp = {"token": ui.token, "bio": bio}
                    join_msg = json.dumps(temp)
                    send1 = sock.makefile('w')
                    recv = sock.makefile('r')

                    send1.write(join_msg + '\r\n')
                    send1.flush()

                    resp = recv.readline()
                    resp = extract_json(resp)
                    print(f'\n{resp.message}.')
                    if resp.type == 'error':
                        return False
    except (ConnectionError, TimeoutError) as connection_error:
        if not user_interface.admin_mode:
            print('Connection Error. Please re-examine your connection.')
        return False

    return True


# if __name__ == "__main__":
#     print(send('168.235.86.101', 3021, "kk", '12345l6789', 'Hi', 'hi'))
