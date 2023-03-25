"""
Mark Nguyen
markvn@uci.edu
84257566
"""

import socket
import json
import ds_protocol


def basic_send(server: str, port: int, username: str, password: str,
               token=False, request=None):
    """Basic request for server"""
    try:
        assert isinstance(server, str), 'Type server is not a string.'
        assert server
        assert isinstance(port, int), 'Type port is not a integer.'
        assert 1 <= port <= 65535, 'Port number limit bypassed.'
        assert isinstance(username, str)
        assert username  # checks that username is not empty
        assert ' ' not in username, 'Username cannot contain any whitespace.'
        assert isinstance(password, str)
        assert password  # checks that password is not empty
        assert ' ' not in password, 'Password cannot contain any whitespace.'
    except AssertionError:
        return False

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server, port))
            if token:
                temp = {"join": {'username': username, 'password': password,
                                 'token': ''}}

                join_msg = json.dumps(temp)
                send1 = sock.makefile('w')
                recv = sock.makefile('r')
                send1.write(join_msg + '\r\n')
                send1.flush()
                resp = recv.readline()
                resp = ds_protocol.extract_json(resp)

                return resp

            if not token:
                send1 = sock.makefile('w')
                recv = sock.makefile('r')

                send1.write(request + '\r\n')
                send1.flush()

                resp = recv.readline()
                return resp

    except (ConnectionError, TimeoutError, socket.gaierror):
        print('Connection Error. Please re-examine your connection.')
        return False
