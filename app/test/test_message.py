import pytest
from app.main.message import Message


@pytest.mark.parametrize('sender,receiver,message,subject,expected', [
    (
        "Dummy Sender", "Dummy Receiver", "This is a message test",
        "Test Message", True
    ),
    (
        "", "Dummy Receiver", "This is a message test", "Test Message", False
    ),
    (
        "Dummy Sender", "", "This is a message test", "Test Message", False
    ),
    (
        "Dummy Sender", "Dummy Receiver", "", "Test Message", False
    ),
    (
        "Dummy Sender", "", "This is a message test", "", False
    ),
    (
        "", "", "", "", False
    )
])
def test_validate_inputs(sender, receiver, message, subject, expected):
    ret = Message.validate_inputs(sender, receiver, message, subject)
    assert ret == expected


@pytest.mark.parametrize('message,expected', [
    (
            Message("Dummy Sender", "Dummy Receiver", "This is a test message",
                    "Test Message"),
            {
                "sender": "Dummy Sender",
                "receiver": "Dummy Receiver",
                "message": "This is a test message",
                "subject": "Test Message"
            }
    )
])
def test_to_json(message, expected):
    ret = message.to_json()
    if 'creation_date' not in ret.keys():
        pytest.fail("No creation date was set.")
    del ret['creation_date']

    if 'uid' not in ret.keys():
        pytest.fail("No uid was set.")
    del ret['uid']
    assert ret == expected


@pytest.mark.parametrize('json_dict,expected', [
    (
            {
                "sender": "Dummy Sender",
                "receiver": "Dummy Receiver",
                "message": "This is a test message",
                "subject": "Test Message"
            },
            Message("Dummy Sender", "Dummy Receiver", "This is a test message",
                    "Test Message")
    )
])
def test_to_json(json_dict, expected):
    message = Message.from_dict(json_dict)
    assert message.sender == expected.sender
    assert message.receiver == expected.receiver
    assert message.message == expected.message
    assert message.subject == expected.subject

