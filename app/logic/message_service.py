from flask import jsonify, make_response

from app.main.message import Message, MessageValidationError
from db.message_store import MessageStore, MessageNotFound

message_store = MessageStore()


def write_message(json_dict):
    try:
        message = Message.from_dict(json_dict)
    except MessageValidationError as mve:
        return custom_error(mve.__str__(), 400)
    if message:
        return jsonify(message_store.store(message))


def get_message_by_receiver(receiver, unread):
    if unread:
        unread = str_to_bool(unread.upper())
        if unread:
            messages = message_store.load_by_receiver(receiver, unread=unread)
        else:
            return custom_error("Invalid unread value.", 400)
    else:
        messages = message_store.load_by_receiver(receiver)
    if messages:
        return jsonify(messages)
    return custom_error("No Unread message found.", 404)


def get_message_by_id(message_id):
    message = message_store.load_by_id(message_id)
    if message:
        return jsonify(message)


def delete_message_by_id(message_id):
    try:
        message = message_store.delete(message_id)
    except MessageNotFound as mnf:
        return custom_error(mnf.__str__(), 404)
    if message:
        return jsonify(message)


def custom_error(message, status_code):
    return make_response(jsonify(message), status_code)


def str_to_bool(bool_str):
    if bool_str == 'TRUE':
        return True
    elif bool_str == 'FALSE':
        return False
    else:
        return None