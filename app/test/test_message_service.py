import pytest
from db import get_db, init_db
import app.logic.message_service as ms


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
def test_write_message(json_dict, expected, tmp_path):
    db = get_db(tmp_path / 'db.db')
    db.execute('''CREATE TABLE message( id INTEGER PRIMARY KEY,
                sender text, receiver text, message text, subject text, 
                date date, unread INTEGER)''')

    ms.write_message(json_dict)

