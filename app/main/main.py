from app.main.message import MessageStoreError
from db import init_db
from flask import g, request, session, make_response, jsonify
from app.main import create_app
from app.logic import message_service as ms
from app.logic import user_service as us
import os
import tempfile

app = create_app(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def create_db_file():
    """

    :rtype: str
    :return:
    """
    temp_db_path = tempfile.NamedTemporaryFile().name
    app.logger.info('Database path: {0}'.format(temp_db_path))
    return temp_db_path


db_path = create_db_file()
app.config['DATABASE'] = db_path
with app.app_context():
    init_db()


# Post Create message
@app.route('/messages/new', methods=['POST'])
def write_message():
    """
    Create a message in message table.

    :rtype: flask.wrappers.Response
    :return: The created message
    """
    json_dict = request.get_json()
    if not us.validate_users(json_dict):
        return make_response(jsonify("Sender or receiver is not found."), 404)
    try:
        message = ms.write_message(json_dict)
        return make_response(jsonify(message), 200)
    except MessageStoreError as e:
        if e.error == MessageStoreError.INVALID:
            return make_response(MessageStoreError.INVALID, 400)


# Get all messages from a specific user without authentication
# @app.route('/messages/<receiver>', methods=['GET'])
# def get_message(receiver):
#     if us.query_user(receiver):
#         unread = request.args.get('unread')
#         return ms.get_message_by_receiver(receiver, unread)
#     return make_response(jsonify("Receiver is not found."), 404)


# Get all messages from a specific user with authentication
@app.route('/messages', methods=['GET'])
def get_message_auth():
    """
    Search all messages where the receiver is the user in the session.
    if the unread arg is set to true, return only the unread messages.

    :rtype: flask.wrappers.Response
    :return: The requested message.
    """
    # Check if user was deleted during the session.
    if us.query_user(session['user_name']):
        unread = request.args.get('unread', 'false')
        try:
            return jsonify(ms.get_message_by_receiver(session['user_name'],
                                                      unread))
        except MessageStoreError as e:
            if e.error == MessageStoreError.NO_UNREAD_MESSAGES:
                return make_response(jsonify(
                    MessageStoreError.NO_UNREAD_MESSAGES), 200)
    return make_response(jsonify("Receiver is not found."), 404)


# get and delete
@app.route('/message/<message_id>', methods=['GET', 'DELETE'])
def get_or_delete_message_by_id(message_id):
    """
    GET : Search a message with a matching ID and return it.
    DELETE : Search a message with a matching ID, delete it and return it.

    :param str message_id: The id of the message.
    :rtype: flask.wrappers.Response
    :return: A message with the matching ID number.
    """
    try:
        if request.method == 'GET':
            return jsonify(ms.get_message_by_id(message_id))
        if request.method == 'DELETE':
            return ms.delete_message_by_id(message_id)
    except MessageStoreError as e:
        if e.error == MessageStoreError.NOT_FOUND:
            return make_response(jsonify(MessageStoreError.NOT_FOUND), 404)


@app.teardown_appcontext
def close_connection(_):
    """
    Closes the connection to the db.
    Should be called when the applications context ends.

    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5000)
