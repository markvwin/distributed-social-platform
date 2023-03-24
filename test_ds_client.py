"""
Mark Nguyen
markvn@uci.edu
84257566
"""
import socket

import ds_client
import time
import json
import ds_protocol
import pytest
import socket


def test_basic_send_get_token():
    ip = "168.235.86.101"
    port = 3021
    user = "pytestaccount"
    pwd = "123456789"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert resp.type == 'ok'


def test_basic_send_non_token():
    ip = "168.235.86.101"
    port = 3021
    user = "pytestaccount"
    pwd = "123456789"
    recip = "pytestaccount"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    token = resp.token
    req = {"token": token, "directmessage": {"entry": 'hi', "recipient": recip,
                                             "timestamp": time.time()}}
    req = json.dumps(req)
    resp = ds_client.basic_send(ip, port, user, pwd, request=req)
    resp = ds_protocol.extract_json(resp)
    assert resp.type == 'ok'


def test_basic_send_exception():
    ip = "168.235.86.10"
    port = 3021
    user = "pytestaccount"
    pwd = "123456789"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_server_assert():
    ip = 123
    port = 3021
    user = "pytestaccount"
    pwd = "123456789"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_server_not_none_assert():
    ip = ''
    port = 3021
    user = "pytestaccount"
    pwd = "123456789"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_port_assert_is_int():
    ip = '168.235.86.101'
    port = 'not a int'
    user = "pytestaccount"
    pwd = "123456789"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_port_assert_is_in_range():
    ip = '168.235.86.101'
    port = 999999999999999999
    user = "pytestaccount"
    pwd = "123456789"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_user_not_none():
    ip = '168.235.86.101'
    port = 3021
    user = ""
    pwd = "123456789"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_user_is_str():
    ip = '168.235.86.101'
    port = 3021
    user = ['not a string']
    pwd = "123456789"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_no_space_in_user():
    ip = '168.235.86.101'
    port = 3021
    user = "pytest account"
    pwd = '123456789'
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_pass_is_str():
    ip = '168.235.86.101'
    port = 3021
    user = "pytestaccount"
    pwd = 123456789
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_pass_is_not_none():
    ip = '168.235.86.101'
    port = 3021
    user = "pytestaccount"
    pwd = ''
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_no_space_in_pass():
    ip = '168.235.86.101'
    port = 3021
    user = "pytestaccount"
    pwd = ' '
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert not resp


def test_ds_client_workds():
    ip = "168.235.86.101"
    port = 3021
    user = "pytestaccount"
    pwd = "123456789"
    resp = ds_client.basic_send(ip, port, user, pwd, token=True)
    assert resp
