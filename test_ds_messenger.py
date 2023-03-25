"""
Mark Nguyen
markvn@uci.edu
84257566
"""

import ds_messenger as dm
import time
import Profile
from pathlib import Path


def test_direct_message_instantiation():
    recip = 'tester'
    msg = 'iamatester'
    timestamp = time.time()
    dm_obj = dm.DirectMessage()
    dm_obj.recipient = recip
    dm_obj.message = msg
    dm_obj.timestamp = timestamp
    test_list = [dm_obj.recipient, dm_obj.message, dm_obj.timestamp]
    assert test_list == [recip, msg, timestamp]


def test_dm_check_response_success():
    ip = '168.235.86.101'
    user = 'tester'
    pwd = 'iamatester'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    resp = dm_obj.check_response()
    assert resp


def test_dm_check_response_failure():
    ip = 'not a valid ip'
    user = 'tester'
    pwd = 'iamatester'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    resp = dm_obj.check_response()
    assert not resp


def test_dm_get_token():
    ip = '168.235.86.101'
    user = 'tester99999999'
    pwd = 'iamatester'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    token = dm_obj.get_token()
    assert token


def test_dm_get_token_failure():
    ip = '168.235.86.101'
    user = 'tester99999999'
    pwd = 'notthecorrectpassword'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    token = dm_obj.get_token()
    assert not token


def test_dm_get_token_no_response():
    ip = 'not a valid ip'
    port = 3021
    user = 'tester'
    pwd = 'iamatester'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    token = dm_obj.get_token()
    assert not token


def test_dm_get_token_error_response():
    ip = '168.235.86.101'
    port = 3021
    user = 'tester'
    pwd = 'iam a tester'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    token = dm_obj.get_token()
    assert not token


def test_dm_send_no_token():
    ip = '168.235.86.101'
    user = 'tester 99999999'
    pwd = 'iamatester'
    msg = 'hi'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    resp = dm_obj.send(msg, user)
    assert not resp


def test_dm_send():
    ip = '168.235.86.101'
    user = 'tester99999999'
    pwd = 'iamatester'
    msg = 'hi'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    current_prof = Profile.Profile(ip, user, pwd)
    Profile.LOGGED_IN = True
    Profile.PROFILE_DIRECTORY = 'test00.dsu'
    path = Path('test00.dsu')
    path.touch()
    current_prof.save_profile('test00.dsu')
    resp = dm_obj.send(msg, user)
    assert resp


def test_dm_retrieve_new():
    ip = '168.235.86.101'
    user = 'tester99999999'
    pwd = 'iamatester'
    msg = 'hi'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    current_prof = Profile.Profile(ip, user, pwd)
    Profile.LOGGED_IN = True
    Profile.PROFILE_DIRECTORY = 'test00.dsu'
    path = Path('test00.dsu')
    path.touch()
    current_prof.save_profile('test00.dsu')
    resp = dm_obj.retrieve_new()
    assert isinstance(resp, list)


def test_dm_retrieve_all():
    ip = '168.235.86.101'
    user = 'tester99999999'
    pwd = 'iamatester'
    msg = 'hi'
    dm_obj = dm.DirectMessenger(ip, user, pwd)
    current_prof = Profile.Profile(ip, user, pwd)
    Profile.LOGGED_IN = True
    Profile.PROFILE_DIRECTORY = 'test00.dsu'
    path = Path('test00.dsu')
    path.touch()
    current_prof.save_profile('test00.dsu')
    resp = dm_obj.retrieve_all()
    assert isinstance(resp, list)
