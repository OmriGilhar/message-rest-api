import pytest
from db import init_db
import tempfile
from app.main.main import app
import os


@pytest.fixture(scope='function')
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='function')
def create_message(client):
    name_1 = 'DummySender1'
    name_2 = 'DummySender2'
    user_1_json = {
        "user_name": name_1,
        "password": "asasdaNKJABDS"
    }

    user_2_json = {
        "user_name": name_2,
        "password": "83hf83hf8"
    }
    client.post('auth/register', json=user_1_json)
    client.post('auth/register', json=user_2_json)

    test_json = {
        "sender": name_1,
        "receiver": name_2,
        "message": "This is a test message",
        "subject": "Test Message"
    }
    rv = client.post('/messages/new', json=test_json)
    test_json['unread'] = 0
    returned_json = rv.json[0]
    return test_json, returned_json


def test_post_valid_message(create_message):
    """Start with a blank database."""

    test_json, returned_json = create_message
    assert (
        'creation_date' in returned_json
        and returned_json['creation_date'] != ''
    )
    del returned_json['creation_date']
    assert 'uid' in returned_json and isinstance(returned_json['uid'], int)
    del returned_json['uid']
    assert returned_json == test_json


def test_get_message_by_valid_user(client, create_message):
    """Start with a blank database."""
    test_json, returned_json = create_message
    rv = client.get('/messages/Dummy%20Receiver')
    returned_json = rv.json[0]
    assert 'creation_date' in returned_json and returned_json[
        'creation_date'] != ''
    del returned_json['creation_date']
    assert 'uid' in returned_json and isinstance(returned_json['uid'], int)
    del returned_json['uid']
    assert returned_json == test_json


def test_get_all_unread_message_by_valid_user(client, create_message):
    """Start with a blank database."""
    test_json, returned_json = create_message
    rv = client.get('/messages/Dummy%20Receiver?unread=true')
    returned_json = rv.json[0]
    assert 'creation_date' in returned_json and returned_json[
        'creation_date'] != ''
    del returned_json['creation_date']
    assert 'uid' in returned_json and isinstance(returned_json['uid'], int)
    del returned_json['uid']
    assert returned_json == test_json
    rv = client.get('/messages/Dummy%20Receiver?unread=true')
    assert rv.status_code == 404


def test_get_message_by_valid_message_id(client, create_message):
    """Start with a blank database."""

    test_json, returned_json = create_message
    rv = client.get('/message/{0}'.format(returned_json['uid']))
    returned_message = rv.json[0]
    assert 'creation_date' in returned_message and returned_message[
        'creation_date'] != ''
    del returned_message['creation_date']
    assert 'uid' in returned_message and isinstance(returned_message['uid'],
                                                    int)
    del returned_message['uid']
    assert returned_message == test_json


def test_delete_message_by_valid_message_id(client, create_message):
    """Start with a blank database."""

    test_json, returned_json = create_message
    rv = client.delete('/message/{0}'.format(returned_json['uid']))
    returned_message = rv.json[0]
    assert 'creation_date' in returned_message and returned_message[
        'creation_date'] != ''
    del returned_message['creation_date']
    assert 'uid' in returned_message and isinstance(returned_message['uid'],
                                                    int)
    del returned_message['uid']
    assert returned_message == test_json
