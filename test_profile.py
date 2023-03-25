"""
Mark Nguyen
markvn@uci.edu
84257566
"""

import Profile
import time
import ds_messenger
from pathlib import Path
import pytest


def test_post_object():
    """checks that post-entry is not none and post object is instantiated"""
    timestamp = time.time()
    entry = 'HIII'
    post = Profile.Post(entry)
    post.set_time(timestamp)

    assert post.get_time() != 0
    assert post.get_entry()


def test_profile_object():
    """checks that post-entry is not none and post object is instantiated"""
    ip = '168.235.86.101'
    user = 'tester99999999'
    pwd = 'iamatester'
    bio = 'bio of a tester'
    path = 'test00.dsu'
    timestamp = time.time()

    dm = ds_messenger.DirectMessage()
    dm.recipient = user
    dm.message = 'hi'
    dm.timestamp = timestamp

    entry = 'HIII'
    post = Profile.Post(entry, timestamp)
    post_two = Profile.Post(entry, 123)

    prof = Profile.Profile(ip, user, pwd)
    prof.bio = bio

    assert prof.dsuserver
    assert prof.username
    assert prof.password
    assert prof.bio

    prof.messages.append(dm.__dict__)
    prof.add_post(post)
    prof.add_post(post_two)
    assert post in prof.get_posts()
    prof.del_post(0)
    assert post not in prof.get_posts()
    prof.my_messages.append(dm.__dict__)
    prof.friends.append('itsameemario')

    if not Path(path):
        Path(path).touch()
    prof.save_profile(path)

    temp_prof = Profile.Profile()
    temp_prof.load_profile(path)
    temp_list = [temp_prof.username, temp_prof.password, temp_prof.dsuserver,
                 temp_prof.bio, temp_prof.messages, temp_prof.my_messages,
                 temp_prof.friends]
    temp_prof.del_post(0)

    assert None not in temp_list
    assert [] not in temp_list


def test_profile_index_error():
    prof = Profile.Profile()
    resp = prof.del_post(1)
    assert not resp


def test_profile_save_exception():
    with pytest.raises(Profile.DsuFileError):
        ip = '168.235.86.101'
        user = 'tester99999999'
        pwd = 'iamatester'
        bio = 'bio of a tester'
        path = 'test00.dsu'
        timestamp = time.time()

        dm = ds_messenger.DirectMessage()
        dm.recipient = user
        dm.message = 'hi'
        dm.timestamp = timestamp

        if not Path(path):
            Path(path).touch()

        temp_prof = Profile.Profile()
        temp_prof.my_messages.append(dm)
        temp_prof.save_profile(path)


def test_profile_save_not_dsu():
    with pytest.raises(Profile.DsuFileError):
        path = 'test00.txt'
        if not Path(path):
            Path(path).touch()
        temp_prof = Profile.Profile()
        temp_prof.save_profile(path)


def test_prof_load_exception():
    with pytest.raises(Profile.DsuProfileError):
        path = 'test00.dsu'
        if not Path(path):
            Path(path).touch()
        temp_prof = Profile.Profile()
        temp_prof._posts.append('hi')
        temp_prof.save_profile(path)
        temp_prof.load_profile(path)


def test_prof_load_not_dsu():
    with pytest.raises(Profile.DsuFileError):
        path = 'test00.txt'
        if not Path(path):
            Path(path).touch()
        temp_prof = Profile.Profile()
        temp_prof._posts.append('hi')
        temp_prof.load_profile(path)
