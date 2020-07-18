from db import init_db
from flask import g, request, session
from app.main import create_app
from app.logic import message_service as ms
import os
import tempfile

app = create_app(__name__)
# TODO: generate 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def create_db_file():
    """


    :rtype: str
    :return:
    """
    return os.path.join(tempfile.gettempdir(), "temp.db")


db_path = create_db_file()
app.config['DATABASE'] = db_path
with app.app_context():
    init_db()


# Post Create message
@app.route('/messages/new', methods=['GET', 'POST'])
def write_message():
    if request.method == 'POST':
        json_dict = request.get_json()
        return ms.write_message(json_dict)


# Get all messages from a specific user
@app.route('/messages/<receiver>', methods=['GET', 'POST'])
def get_message(receiver):
    if request.method == 'GET':
        unread = request.args.get('unread')
        return ms.get_message_by_receiver(receiver, unread)


# Auth Get all messages from a specific user
@app.route('/messages', methods=['GET'])
def get_message_auth():
    unread = request.args.get('unread')
    return ms.get_message_by_receiver(session['user_name'], unread)


# get and delete
@app.route('/message/<message_id>', methods=['GET', 'DELETE'])
def get_or_delete_message_by_id(message_id):
    if request.method == 'GET':
        return ms.get_message_by_id(message_id)
    if request.method == 'DELETE':
        return ms.delete_message_by_id(message_id)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5000)
