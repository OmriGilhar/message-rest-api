from app.main.message import Message, MessageStoreError
from db.message_store import MessageStore

message_store = MessageStore()


def write_message(json_dict):
    """
    Prepare and validate the message before storing the message; then store.

    :param dict json_dict:
    :rtype: dict
    :return: The stored message
    :raise: MessageStoreError
    """
    message = Message.from_dict(json_dict)
    return message_store.store(message)


def get_message_by_receiver(receiver, unread):
    """
    Search and return the all the messages with the receiver name.

    :param str receiver: The user who receives the message
    :param str unread: Flag indication for unread messages
    :rtype: list
    :return: A list of messages.
    """
    unread_bool = str_to_bool(unread)
    messages = message_store.load_by_receiver(receiver, unread=unread_bool)
    if not messages:
        raise MessageStoreError(MessageStoreError.NO_UNREAD_MESSAGES)
    return messages


def get_message_by_id(message_id):
    """
    Search for a single message with the matching message id.

    :param str message_id: The message ID
    :rtype: flask.wrappers.Response
    :return: A JSON representation of the message.
    """
    message = message_store.load_by_id(message_id)
    if not message:
        raise MessageStoreError(MessageStoreError.NOT_FOUND)
    return message


def delete_message_by_id(message_id):
    """
    Deleting a message by a message ID.

    :param str message_id:
    :rtype; dict
    :return: The message that has been deleted
    """
    return message_store.delete(message_id)


def str_to_bool(bool_str):
    return bool_str.upper() == 'TRUE'
