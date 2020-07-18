import pytest
from db import get_db, init_db
import tempfile
from app.main.main import app
import os
import app.logic.message_service as ms


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.mark.parametrize('json_dict,expected', [
    (
            {
                "sender": "Dummy Sender",
                "receiver": "Dummy Receiver",
                "message": "This is a test message",
                "subject": "Test Message"
            },
            {
                "message": "This is a test message",
                "receiver": "Dummy Receiver",
                "sender": "Dummy Sender",
                "subject": "Test Message",
                "unread": 0
            }
    )
])
def test_write_message(json_dict, expected, client):
    ms.write_message(json_dict)

